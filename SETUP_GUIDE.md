# DiagnoSure - Comprehensive Healthcare AI Platform

## 🎯 Overview

DiagnoSure is an end-to-end healthcare platform that integrates:
- **AI Symptom Checker** - Intelligent symptom analysis with potential condition suggestions
- **OCR Prescription Reader** - Extract medicines from prescription images/PDFs
- **Nearby Providers Finder** - Locate hospitals and healthcare providers near you
- **Appointment Management** - Book and manage medical appointments
- **Community Forum** - Share experiences and learn from others
- **Medicine Reminders** - Never miss your medications

---

## 🚀 Quick Start

### Prerequisites
- **Docker** and **Docker Compose** installed
- **Node.js** 16+ (for frontend development)
- **Git** (for version control)

### Option 1: One-Command Setup (Automated)

**Windows:**
```bash
START.bat
```

**Linux/Mac:**
```bash
chmod +x START.sh
./START.sh
```

The script will:
✓ Check Docker installation
✓ Start database and backend services
✓ Run migrations
✓ Install frontend dependencies
✓ Display access URLs

### Option 2: Manual Setup

#### Step 1: Setup Environment Variables
```bash
cd backend
cp ../.env.example .env
# Edit .env with your configuration
```

#### Step 2: Start Backend Services
```bash
docker-compose up -d

# Wait 15 seconds for database
sleep 15

# Run migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

#### Step 3: Start Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                     │
│           (http://localhost:5173)                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Pages:                                          │   │
│  │ - Symptom Checker (ChatWindow)                  │   │
│  │ - Prescription Reader                           │   │
│  │ - Nearby Providers (MapPage)                    │   │
│  │ - Appointments History                          │   │
│  │ - Community Forum                               │   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │
                    API (http://localhost:8090)
                           │
┌──────────────────────────┴──────────────────────────────┐
│              Backend (Django REST)                      │
│         (http://localhost:8090/api)                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Endpoints:                                      │   │
│  │ POST   /symptoms/check/    - Symptom analysis  │   │
│  │ POST   /upload-prescription/ - OCR processing  │   │
│  │ GET    /hospitals/search/  - Find providers    │   │
│  │ POST   /appointments/book/ - Book appointment  │   │
│  │ GET    /appointments/      - List appointments │   │
│  │ GET/POST /forum/posts/     - Community         │   │
│  │ GET    /reminders/list/    - Medicine reminders│   │
│  └─────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼──┐          ┌───▼────┐        ┌───▼──┐
   │  DB   │          │  Cache │        │Celery│
   │  Postgres         Redis             Task
   │ Port 5432│        Port 6379│       Queue │
   └────────┘          └────────┘        └─────┘
```

---

## 🔌 API Endpoints

### Symptom Checker
**POST** `/api/symptoms/check/`
```json
Request:
{
  "symptoms": "I have a cough and cold"
}

Response:
{
  "success": true,
  "input_symptoms": "I have a cough and cold",
  "plain_text_summary": "...",
  "potential_conditions": [...],
  "medical_research": [...],
  "past_case_studies": [...]
}
```

### Prescription Upload (OCR)
**POST** `/api/upload-prescription/`
```
multipart/form-data:
- file: image or PDF

Response:
{
  "success": true,
  "medicines": [
    {
      "name": "Amoxicillin",
      "dosage": "500mg",
      "uses": "Antibiotic",
      "confidence": 0.95
    }
  ]
}
```

### Hospital Search
**GET** `/api/hospitals/search/?lat=40.7128&lon=-74.0060&query=hospital`

### Appointments
**POST** `/api/appointments/book/` - Book appointment
**GET** `/api/appointments/` - List appointments
**POST** `/api/appointments/cancel/{id}/` - Cancel appointment

### Forum
**GET** `/api/forum/posts/` - List posts
**POST** `/api/forum/posts/` - Create post
**GET** `/api/forum/posts/{id}/` - Get post detail
**POST** `/api/forum/posts/{id}/` - Add comment

---

## 🛠️ Docker Management

### View Logs
```bash
# Backend logs
docker-compose logs web -f

# All services
docker-compose logs -f

# Specific service
docker-compose logs db
docker-compose logs redis
```

### Access Database
```bash
# Enter PostgreSQL container
docker-compose exec db psql -U postgres -d healthcare

# Common queries
\dt                    # List tables
SELECT * FROM core_appointment;
SELECT * FROM core_extractedmedicine;
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove data
docker-compose down -v
```

### Rebuild Containers
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 📁 Project Structure

```
DiagnoSure-1/
├── backend/
│   ├── core/                    # Main app
│   │   ├── views.py            # API endpoints
│   │   ├── urls.py             # URL routing
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── ai_model/
│   │   │   └── extractor.py    # OCR/Medicine extraction
│   │   └── migrations/         # DB migrations
│   ├── healthcare_backend/      # Django config
│   │   ├── settings.py         # Settings
│   │   ├── urls.py             # Root URL config
│   │   └── celery.py           # Async tasks
│   ├── docker-compose.yml      # Docker services
│   ├── dockerfile              # Docker image
│   ├── requirements.txt        # Python dependencies
│   └── manage.py              # Django CLI
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatWindow.jsx  # Symptom checker
│   │   │   ├── PrescriptionReader.jsx  # OCR
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── ConditionCard.jsx
│   │   │   └── ...
│   │   ├── pages/              # Page routes
│   │   │   ├── MapPage/        # Providers map
│   │   │   ├── AppointmentsPage/
│   │   │   ├── Profile/
│   │   │   └── ...
│   │   ├── api/
│   │   │   └── api.js          # API wrappers
│   │   ├── context/
│   │   │   └── AppContext.jsx  # Global state
│   │   ├── utils/
│   │   │   ├── mockData.js
│   │   │   └── translations.js
│   │   └── App.jsx             # Root component
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── model/
│   ├── diagnosis.py            # Diagnosis logic
│   ├── symptoms.py             # Symptom processing
│   ├── agent.py                # AI agents
│   └── prescriptionReader/     # OCR implementation
│
├── START.bat                    # Windows startup
├── START.sh                     # Linux/Mac startup
├── .env.example                 # Environment template
└── README.md                    # This file
```

---

## 🔧 Configuration Guide

### Environment Variables (.env)

```bash
# Django settings
SECRET_KEY=your-secret-key
DEBUG=True  # Set to False in production
ALLOWED_HOSTS=*

# Database
POSTGRES_DB=healthcare
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# JWT/Auth
SIMPLE_JWT_SECRET_KEY=your-jwt-secret

# External APIs
GOOGLE_CLIENT_ID=your-google-id
HUGGINGFACE_API_TOKEN=your-token
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

### Docker Compose Services

**Web (Django Backend)**
- Runs on port 8090
- Auto-reloads on code changes
- Depends on db and redis

**Database (PostgreSQL)**
- Runs on port 5432
- Persists data in `postgres_data` volume

**Redis**
- Runs on port 6379
- Used for caching and Celery tasks

**Celery (Async Tasks)**
- Processes background jobs
- Requires Redis connection

---

## 🧪 Testing Features

### Test Symptom Checker
1. Go to http://localhost:5173/symptom-checker
2. Type: "I have a cough and cold"
3. View potential conditions, research, and case studies

### Test Prescription Reader
1. Go to http://localhost:5173/prescription-reader
2. Upload an image or PDF
3. View extracted medicines and analysis

### Test Nearby Providers
1. Go to http://localhost:5173/map
2. Allow location access
3. Search for hospitals nearby

### Test Appointments
1. Go to http://localhost:5173/appointments
2. Book appointment from hospital details
3. View in appointments history

---

## 🐛 Troubleshooting

### Docker containers won't start
```bash
# Check if ports are in use
netstat -an | grep 8090   # Windows
lsof -i :8090             # Mac/Linux

# Kill process using port
# Windows: taskkill /PID <PID> /F
# Mac/Linux: kill -9 <PID>
```

### Database migration errors
```bash
# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Frontend not connecting to backend
- Ensure backend is running: `docker-compose logs web`
- Check BASE_URL in `frontend/src/api/api.js`
- Verify CORS settings in `backend/healthcare_backend/settings.py`

### Memory issues
```bash
# Increase Docker memory
# Edit Docker Desktop settings or docker-compose.yml
services:
  web:
    mem_limit: 2g
```

### Port conflicts
Change ports in docker-compose.yml:
```yaml
ports:
  - "8091:8000"  # Change 8090 to 8091
```

---

## 📊 Key Features Explained

### 1. Symptom Checker
- **Input**: User describes symptoms
- **Processing**: Backend analyzes symptoms using keyword matching
- **Output**: Potential conditions with confidence scores, research articles, case studies
- **Integration**: ChatWindow.jsx → `/api/symptoms/check/` → get_symptom_diagnosis()

### 2. OCR Prescription Reader
- **Input**: Upload image or PDF of prescription
- **Processing**: MedicineExtractor extracts text → matches medicines → confidence scoring
- **Output**: List of medicines with dosage, uses, descriptions
- **Integration**: PrescriptionReader.jsx → `/api/upload-prescription/` → extractor.py

### 3. Nearby Providers
- **Input**: User location (lat/lon) + search query
- **Processing**: Nominatim API searches for providers within radius
- **Output**: Markers on map with provider info and booking button
- **Integration**: MapPage.jsx → `/api/hospitals/search/` → Nominatim REST API

### 4. Appointment System
- **Input**: Provider details, doctor name, date, time, symptoms
- **Processing**: Saves to Appointment model
- **Output**: Confirmation, appointment ID, reminders
- **Integration**: AppointmentForm.jsx → `/api/appointments/book/`

### 5. Medicine Reminders
- **Input**: Appointment or prescription medicines
- **Processing**: Creates Reminder objects with scheduled time
- **Output**: Notification at scheduled time (via Twilio/FCM)
- **Integration**: Triggered after prescription upload or appointment booking

---

## 🚀 Production Deployment

### Before deploying:
1. Set `DEBUG=False` in .env
2. Generate strong `SECRET_KEY`
3. Set `ALLOWED_HOSTS` to your domain
4. Use environment-specific configuration
5. Set up HTTPS (SSL/TLS)
6. Configure proper database backups
7. Use production-grade database (not SQLite)

### Deploy with Docker:
```bash
# Pull latest code
git pull origin main

# Build and push images
docker build -t my-registry/diagnosure-backend .
docker push my-registry/diagnosure-backend

# Update docker-compose.yml with new image
# Deploy to production
docker-compose up -d
```

---

## 📞 Support & Contributing

For issues, questions, or contributions:
1. Check existing issues
2. Review troubleshooting section
3. Check Docker logs
4. Test endpoints with Postman/curl
5. Open an issue with error logs

---

## 📝 License

This project is licensed under MIT License.

---

## 🙏 Acknowledgments

- Built with Django, React, PostgreSQL, and Docker
- Uses Nominatim for location services
- Implements OpenAI/HuggingFace for NLP
- Community-driven healthcare platform

---

**Version**: 1.0.0
**Last Updated**: 2026-04-10
