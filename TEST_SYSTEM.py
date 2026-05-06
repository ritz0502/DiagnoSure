#!/usr/bin/env python3
"""
DiagnoSure System Validation Script
Tests all critical endpoints and features
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8090"
API_URL = f"{BASE_URL}/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(title):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{Colors.RESET}\n")

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def test_backend_health():
    """Test if backend is running"""
    print_header("1. Testing Backend Health")
    try:
        response = requests.get(f"{API_URL}/home/", timeout=5)
        if response.status_code == 200:
            print_success(f"Backend is running at {BASE_URL}")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to backend at {BASE_URL}")
        print_warning("Make sure Docker containers are running: docker-compose up -d")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def test_symptom_checker():
    """Test symptom checking endpoint"""
    print_header("2. Testing Symptom Checker")
    try:
        payload = {
            "symptoms": "I have a cough and cold with sinus pressure"
        }
        response = requests.post(f"{API_URL}/symptoms/check/", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Symptom checker endpoint working")
                if "potential_conditions" in data:
                    conditions = data["potential_conditions"]
                    print(f"  Found {len(conditions)} potential conditions:")
                    for i, cond in enumerate(conditions[:3], 1):
                        confidence = cond.get("confidence", 0) * 100
                        print(f"    {i}. {cond['name']} ({confidence:.0f}% confidence)")
                return True
            else:
                print_error(f"Symptom checker returned error: {data.get('error')}")
                return False
        else:
            print_error(f"Symptom checker returned status {response.status_code}")
            print_warning(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error testing symptom checker: {str(e)}")
        return False

def test_hospital_search():
    """Test hospital search endpoint"""
    print_header("3. Testing Hospital Search")
    try:
        # Test with sample coordinates (New York City)
        lat, lon = 40.7128, -74.0060
        params = {
            "lat": lat,
            "lon": lon,
            "query": "hospital"
        }
        response = requests.get(f"{API_URL}/hospitals/search/", params=params, timeout=10)
        
        if response.status_code == 200:
            hospitals = response.json()
            print_success(f"Hospital search working")
            print(f"  Found {len(hospitals)} hospitals near ({lat}, {lon})")
            if len(hospitals) > 0:
                print(f"  Top result: {hospitals[0].get('name', 'Unknown')}")
            return True
        else:
            print_error(f"Hospital search returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing hospital search: {str(e)}")
        return False

def test_appointment_booking():
    """Test appointment booking"""
    print_header("4. Testing Appointment Booking")
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        payload = {
            "doctor_name": "Dr. Test Smith",
            "hospital_name": "Test Medical Center",
            "date": tomorrow,
            "time": "14:00",
            "symptoms": "Routine checkup"
        }
        response = requests.post(f"{API_URL}/appointments/book/", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print_success("Appointment booking working")
                appointment_id = data.get("appointment", {}).get("id")
                print(f"  Appointment created: ID {appointment_id}")
                return True, appointment_id
            else:
                print_error(f"Booking failed: {data.get('errors')}")
                return False, None
        else:
            print_error(f"Booking returned status {response.status_code}")
            return False, None
    except Exception as e:
        print_error(f"Error testing appointment booking: {str(e)}")
        return False, None

def test_list_appointments():
    """Test listing appointments"""
    print_header("5. Testing List Appointments")
    try:
        response = requests.get(f"{API_URL}/appointments/", timeout=10)
        
        if response.status_code == 200:
            appointments = response.json()
            print_success("List appointments working")
            print(f"  Total appointments: {len(appointments)}")
            if len(appointments) > 0:
                latest = appointments[-1]
                print(f"  Latest: {latest.get('doctor_name')} at {latest.get('hospital_name')}")
            return True
        else:
            print_error(f"List appointments returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error listing appointments: {str(e)}")
        return False

def test_list_reminders():
    """Test listing reminders"""
    print_header("6. Testing Reminders System")
    try:
        response = requests.get(f"{API_URL}/reminders/list/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            reminders = data.get("reminders", [])
            print_success("Reminders system working")
            print(f"  Total reminders: {len(reminders)}")
            if len(reminders) > 0:
                print(f"  Latest reminder types: {[r.get('type') for r in reminders[:3]]}")
            return True
        else:
            print_error(f"List reminders returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error listing reminders: {str(e)}")
        return False

def test_forum_posts():
    """Test forum posting"""
    print_header("7. Testing Forum System")
    try:
        response = requests.get(f"{API_URL}/forum/posts/", timeout=10)
        
        if response.status_code == 200:
            posts = response.json()
            print_success("Forum posts listing working")
            print(f"  Total posts: {len(posts)}")
            if len(posts) > 0:
                latest_post = posts[0]
                print(f"  Latest post: '{latest_post.get('title', 'Unknown')}'")
            return True
        else:
            print_error(f"Forum posts returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing forum: {str(e)}")
        return False

def run_all_tests():
    """Run all validation tests"""
    print(f"\n{Colors.BLUE}")
    print("""
    ╔═════════════════════════════════════════╗
    ║   DiagnoSure System Validation Test      ║
    ║   Testing all critical endpoints         ║
    ╚═════════════════════════════════════════╝
    """)
    print(f"Timestamp: {datetime.now()}{Colors.RESET}\n")
    
    results = {}
    
    # Test 1: Backend health
    if not test_backend_health():
        print_error("\nCannot proceed without backend. Please start services first:")
        print("  Windows: START.bat")
        print("  Linux/Mac: ./START.sh")
        return
    
    # Test 2: Symptom Checker
    results['Symptom Checker'] = test_symptom_checker()
    
    # Test 3: Hospital Search
    results['Hospital Search'] = test_hospital_search()
    
    # Test 4: Appointment Booking
    success, appt_id = test_appointment_booking()
    results['Appointment Booking'] = success
    
    # Test 5: List Appointments
    results['List Appointments'] = test_list_appointments()
    
    # Test 6: Reminders
    results['Reminders System'] = test_list_reminders()
    
    # Test 7: Forum
    results['Forum System'] = test_forum_posts()
    
    # Summary
    print_header("Test Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}\n")
    
    for feature, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}{status}{Colors.RESET}  {feature}")
    
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    
    if passed == total:
        print_success(f"\nAll {total} tests passed! System is working correctly.")
        print("\nYou can now:")
        print("  - Visit http://localhost:5173 in your browser")
        print("  - Start using the Symptom Checker")
        print("  - Upload prescriptions")
        print("  - Book appointments")
    else:
        print_warning(f"\n{total - passed} test(s) failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("  - Ensure Docker containers are running: docker-compose logs")
        print("  - Check backend logs: docker-compose logs web")
        print("  - Verify database is ready: docker-compose logs db")
    
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nUnexpected error: {str(e)}")
        sys.exit(1)
