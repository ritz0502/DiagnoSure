from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from .models import UserProfile, Appointment, Reminder, Post, Comment, Category, ExtractedMedicine
from .serializers import (
    UserProfileSerializer,
    AppointmentSerializer,
    PostSerializer,
    CommentSerializer,
    CategorySerializer,
    ExtractedMedicineSerializer,
    ReminderSerializer
)
from .utils import send_notification
from .ai_model.extractor import MedicineExtractor
import tempfile, os
import requests
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view, permission_classes, authentication_classes


extractor = MedicineExtractor()


# -----------------------
# Sample symptom checking response generator
# -----------------------
def get_symptom_diagnosis(symptoms_text):
    """
    Generate a diagnosis response based on symptom input.
    This mimics the mockData structure from the frontend.
    """
    symptoms_lower = symptoms_text.lower()
    
    # Keyword matching to determine response type
    if any(word in symptoms_lower for word in ['cough', 'cold', 'sinus', 'congestion', 'runny nose', 'sore throat']):
        return {
            'plain_text_summary': "Based on your symptoms of cough, cold, and mild sinus issues, you may be experiencing a common upper respiratory infection or seasonal allergies. These symptoms typically indicate inflammation in your nasal passages and throat.",
            'potential_conditions': [
                {
                    'name': 'Common Cold (Viral Upper Respiratory Infection)',
                    'confidence': 0.75,
                    'insights': 'Your symptoms align closely with a typical viral cold. The combination of cough, nasal congestion, and sinus pressure is characteristic of viral upper respiratory infections.',
                    'evidence_links': [
                        {'label': 'CDC Cold Info', 'url': 'https://www.cdc.gov/features/rhinoviruses/'},
                    ]
                },
                {
                    'name': 'Seasonal Allergic Rhinitis',
                    'confidence': 0.65,
                    'insights': 'The mild sinus symptoms combined with cough could indicate seasonal allergies.',
                    'evidence_links': [
                        {'label': 'Allergy Foundation', 'url': 'https://www.aafa.org/allergic-rhinitis/'},
                    ]
                },
                {
                    'name': 'Acute Sinusitis',
                    'confidence': 0.45,
                    'insights': 'While your sinus symptoms are mild, acute sinusitis remains a possibility.',
                    'evidence_links': [
                        {'label': 'ENT Specialists', 'url': 'https://www.entnet.org/content/sinusitis'},
                    ]
                }
            ],
            'medical_research': [
                {
                    'title': 'Viral Upper Respiratory Infections: Current Understanding',
                    'summary': 'Recent research indicates that most upper respiratory infections are self-limiting viral conditions.',
                    'link': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7152197/'
                }
            ],
            'past_case_studies': [
                {
                    'case_id': 'URI-2024-001',
                    'short_summary': '32-year-old patient with similar cold and sinus symptoms recovered fully within 8 days.',
                    'link': 'https://example.com/case-study/uri-001'
                }
            ]
        }
    elif any(word in symptoms_lower for word in ['rash', 'itching', 'itch', 'skin', 'dermatitis']):
        return {
            'plain_text_summary': "Your symptoms of rashes and skin itching suggest a dermatological condition that could range from allergic reactions to eczema or contact dermatitis.",
            'potential_conditions': [
                {
                    'name': 'Contact Dermatitis',
                    'confidence': 0.80,
                    'insights': 'Contact dermatitis is a common cause of itchy rashes, occurring when skin comes into contact with irritants or allergens.',
                    'evidence_links': [
                        {'label': 'AAD Contact Dermatitis', 'url': 'https://www.aad.org/public/diseases/eczema/types/contact-dermatitis'},
                    ]
                },
                {
                    'name': 'Atopic Dermatitis (Eczema)',
                    'confidence': 0.70,
                    'insights': 'Eczema commonly presents with itchy, inflamed skin that may appear as red, scaly patches.',
                    'evidence_links': [
                        {'label': 'National Eczema Assoc', 'url': 'https://nationaleczema.org/eczema/'},
                    ]
                },
                {
                    'name': 'Allergic Reaction',
                    'confidence': 0.60,
                    'insights': 'An allergic reaction could cause widespread itchy rashes, especially if exposed to new substances.',
                    'evidence_links': [
                        {'label': 'ACAAI Skin Allergies', 'url': 'https://acaai.org/allergies/allergic-conditions/skin-allergies/'},
                    ]
                }
            ],
            'medical_research': [
                {
                    'title': 'Management of Chronic Itchy Skin Conditions',
                    'summary': 'Recent studies highlight the importance of identifying triggers and implementing appropriate skincare routines.',
                    'link': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8745231/'
                }
            ],
            'past_case_studies': [
                {
                    'case_id': 'DRM-2024-005',
                    'short_summary': '45-year-old with contact dermatitis from new laundry detergent resolved after switching products.',
                    'link': 'https://example.com/case-study/drm-005'
                }
            ]
        }
    else:
        # Generic response for unknown symptoms
        return {
            'plain_text_summary': f"Based on your reported symptoms, we recommend consulting with a healthcare professional for a proper diagnosis. Please provide more details about your symptoms for better assessment.",
            'potential_conditions': [
                {
                    'name': 'General Medical Consultation Needed',
                    'confidence': 0.50,
                    'insights': 'Your symptoms require professional medical evaluation. Please describe symptoms in more detail.',
                    'evidence_links': []
                }
            ],
            'medical_research': [],
            'past_case_studies': []
        }

# -----------------------
# Home / health check
# -----------------------
def home(request):
    return JsonResponse({"message": "Healthcare Backend is running"})


# -----------------------
# Symptom Checker (ML Model Integration)
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def check_symptoms(request):
    """
    Receive symptoms from user and return potential diagnoses.
    Input: {"symptoms": "user symptom description"}
    Output: Diagnosis with conditions, research, and case studies
    """
    try:
        symptoms_input = request.data.get('symptoms', '').strip()
        
        if not symptoms_input:
            return Response({
                'error': 'Please provide symptom description',
                'success': False
            }, status=400)
        
        # Get diagnosis based on symptoms
        diagnosis = get_symptom_diagnosis(symptoms_input)
        
        return Response({
            'success': True,
            'input_symptoms': symptoms_input,
            **diagnosis
        })
    
    except Exception as e:
        return Response({
            'error': str(e),
            'success': False
        }, status=500)


# -----------------------
# Complete profile (requires login)
# -----------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile updated successfully", "profile": serializer.data})
    return Response(serializer.errors, status=400)


# -----------------------
# Search nearby hospitals (public)
# -----------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def search_hospitals(request):
    query = request.GET.get('query', 'hospital')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    if not lat or not lon:
        return Response({"error": "Latitude and longitude are required"}, status=400)

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return Response({"error": "Invalid latitude or longitude"}, status=400)

    delta = 0.03
    viewbox = f"{lon - delta},{lat - delta},{lon + delta},{lat + delta}"
    url = "https://nominatim.openstreetmap.org/search"
    params = {'q': query, 'format': 'json', 'limit': 20, 'viewbox': viewbox, 'bounded': 1}
    response = requests.get(url, params=params, headers={'User-Agent': 'HealthcareApp'})
    data = response.json()

    results = []
    for item in data:
        results.append({
            "name": item.get("name"),
            "display_name": item.get("display_name"),
            "lat": item.get("lat"),
            "lon": item.get("lon"),
            "osm_id": item.get("osm_id"),
            "type": item.get("type"),
            "class": item.get("class")
        })
    return Response(results)

# -----------------------
# Book Appointment (public or authenticated)
@api_view(['POST'])
@permission_classes([AllowAny])
def book_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        appointment = serializer.save()  # no patient needed
        return Response({'success': True, 'appointment': serializer.data})
    return Response({'success': False, 'errors': serializer.errors}, status=400)
# -----------------------
# List Appointments
# -----------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def list_appointments(request):
    """
    List all appointments.
    """
    appointments = Appointment.objects.all().order_by('-date', '-time')
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# -----------------------
# Cancel Appointment
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def cancel_appointment(request, appointment_id):
    """
    Cancel an appointment by ID.
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found"}, status=404)

    appointment.status = "cancelled"
    appointment.save()
    return Response({"success": True, "message": "Appointment cancelled"})


# -----------------------
# List All Reminders
# -----------------------
@api_view(['GET'])
@permission_classes([AllowAny])
def list_all_reminders(request):
    """
    List all reminders (appointments + prescription).
    """
    appointment_reminders = Reminder.objects.filter(appointment__isnull=False)
    prescription_reminders = Reminder.objects.filter(appointment__isnull=True)

    all_reminders = list(appointment_reminders) + list(prescription_reminders)
    all_reminders.sort(key=lambda r: r.remind_at)

    serializer = ReminderSerializer(all_reminders, many=True)
    return Response({"reminders": serializer.data})
# -----------------------
# Upload prescription (public)
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_prescription(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)

    file = request.FILES['file']
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as temp_file:
        for chunk in file.chunks():
            temp_file.write(chunk)
        file_path = temp_file.name

    try:
        medicines = extractor.extract_medicines_from_image(file_path)
        saved_medicines = []
        for med in medicines:
            obj, _ = ExtractedMedicine.objects.update_or_create(
                name=med.name,
                defaults={
                    'description': med.description,
                    'uses': med.uses,
                    'dosage': med.dosage,
                    'confidence': med.confidence
                }
            )
            saved_medicines.append(obj)

        serializer = ExtractedMedicineSerializer(saved_medicines, many=True)
        return Response({
            'success': True,
            'message': f'{len(saved_medicines)} medicines extracted and saved',
            'medicines': serializer.data
        })

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# -----------------------
# Create prescription reminders (public)
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def create_prescription_reminders(request):
    prescription_items = [
        {"name": "Paracetamol", "dosage": "- 2 times a day"},
        {"name": "Omeprazole", "dosage": "- once before meals"},
        {"name": "Amoxicillin", "dosage": "- 3 times a day"},
        {"name": "Cetirizine", "dosage": "- at night"},
        {"name": "Ibuprofen", "dosage": "- if pain persists"},
    ]
    reminders_created = []
    now = timezone.now()
    for idx, med in enumerate(prescription_items):
        remind_at = now + timedelta(hours=idx + 1)
        Reminder.objects.create(appointment=None, remind_at=remind_at)
        reminders_created.append({
            "medicine": med["name"],
            "dosage": med["dosage"],
            "remind_at": remind_at
        })

    return Response({
        "success": True,
        "message": f"{len(reminders_created)} prescription reminders created",
        "reminders": reminders_created
    })


# -----------------------
# Forum: Posts (public)
# -----------------------
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def posts_list_create(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by("-created_at")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=None)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def post_detail_comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=None, post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def post_vote(request, post_id, action):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    if action == "upvote":
        post.upvotes.clear()
        post.downvotes.clear()
    elif action == "downvote":
        post.upvotes.clear()
        post.downvotes.clear()
    else:
        return Response({"error": "Invalid action"}, status=400)

    return Response({"message": f"{action} recorded", "score": post.score()})


# -----------------------
# Test notifications
# -----------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def test_notify(request):
    message = request.data.get("message", "Test notification from Healthcare backend")
    try:
        send_notification(message)
        return Response({"success": True, "message": "Notification sent"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

