# DiagnoSure - Quick Reference Guide

## 🚀 Getting Started (30 seconds)

### Windows
```bash
START.bat
```

### Mac/Linux
```bash
chmod +x START.sh
./START.sh
```

Then open new terminal:
```bash
cd frontend
npm run dev
```

Visit: http://localhost:5173

---

## 📱 Main Features & URLs

| Feature | URL | Status |
|---------|-----|--------|
| 🏥 Symptom Checker | `/symptom-checker` | ✅ FIXED |
| 📋 Prescription Reader | `/prescription-reader` | ✅ FIXED |
| 🗺️ Nearby Providers | `/map` | ✅ WORKING |
| 📅 Appointments | `/appointments` | ✅ WORKING |
| 👤 Profile | `/profile` | ✅ WORKING |
| 💬 Community | `/communityForum` | ✅ WORKING |

---

## 🔧 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop all
docker-compose down

# Restart specific service
docker-compose restart web

# Execute command in container
docker-compose exec web python manage.py <command>

# View database
docker-compose exec db psql -U postgres -d healthcare
```

---

## 📧 API Testing with curl

### Symptom Check
```bash
curl -X POST http://localhost:8090/api/symptoms/check/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache and fever"}'
```

### Upload Prescription
```bash
curl -X POST http://localhost:8090/api/upload-prescription/ \
  -F "file=@prescription.jpg"
```

### Search Hospitals
```bash
curl "http://localhost:8090/api/hospitals/search/?lat=40.7128&lon=-74.0060&query=hospital"
```

### Book Appointment
```bash
curl -X POST http://localhost:8090/api/appointments/book/ \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_name": "Dr. Smith",
    "hospital_name": "City Hospital",
    "date": "2026-04-20",
    "time": "14:00",
    "symptoms": "Headache"
  }'
```

---

## 🛠️ Common Issues & Fixes

### Backend won't start
```bash
# Check logs
docker-compose logs web

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database error
```bash
# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Frontend can't reach backend
- Check if `http://localhost:8090` is reachable
- Verify CORS is enabled in Django settings
- Check `BASE_URL` in `frontend/src/api/api.js`

### Port already in use
```bash
# Windows
netstat -ano | findstr :8090

# Mac/Linux
lsof -i :8090
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `backend/.env` | Backend configuration |
| `backend/core/views.py` | API endpoints |
| `backend/core/urls.py` | URL routing |
| `frontend/src/api/api.js` | API wrapper functions |
| `frontend/src/components/ChatWindow.jsx` | Symptom checker UI |
| `frontend/src/components/PrescriptionReader.jsx` | OCR/prescription UI |
| `docker-compose.yml` | Service configuration |

---

## 🔗 Direct Links

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8090/api |
| Backend Admin | http://localhost:8090/admin (if configured) |
| Database | localhost:5432 |
| Redis | localhost:6379 |
| Adminer (DB UI) | http://localhost:8080 (if enabled) |

---

## 📊 Database Structure

### Key Tables
- `core_userprofile` - User profiles
- `core_appointment` - Appointments
- `core_extractedmedicine` - Medicines from prescriptions
- `core_reminder` - Medicine/appointment reminders
- `core_post` - Community forum posts
- `core_comment` - Forum comments

### View Data
```bash
docker-compose exec db psql -U postgres -d healthcare

# List appointments
select id, doctor_name, hospital_name, date, time, status from core_appointment;

# List medicines
select name, dosage, confidence from core_extractedmedicine;

# View reminders
select id, remind_at, sent from core_reminder;
```

---

## 🎯 Development Workflow

### Making Changes

1. **Backend Changes**
   ```bash
   # Edit file
   # Changes auto-reload in container
   # Test with curl or Postman
   ```

2. **Frontend Changes**
   ```bash
   cd frontend
   # Edit component
   # Auto-reload in npm dev server
   # Refresh browser
   ```

3. **Database Schema Changes**
   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate
   ```

---

## 🚀 Next Steps

- [ ] Configure OAuth for Google login
- [ ] Set up Twilio for SMS notifications
- [ ] Deploy to production
- [ ] Set up SSL/HTTPS
- [ ] Configure payment system
- [ ] Add real OCR (EasyOCR, Tesseract)
- [ ] Implement advanced symptom analysis (ML models)
- [ ] Add mobile app with React Native

---

## 📞 Need Help?

1. Check SETUP_GUIDE.md for detailed docs
2. Review Docker logs: `docker-compose logs -f`
3. Test backend endpoints directly
4. Check browser console for frontend errors
5. Review API response structures in api.js

---

**Pro Tip**: Keep one terminal open for `docker-compose logs -f` while developing!
