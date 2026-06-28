# 🏥 DiagnoSure

### AI-Powered Healthcare Assistant for Intelligent Diagnosis & Digital Healthcare

> A full-stack healthcare platform that leverages AI, NLP, OCR, and geospatial technologies to provide symptom analysis, prescription digitization, appointment management, hospital discovery, and community healthcare support.

---

## 📌 Overview

DiagnoSure is an AI-driven healthcare platform designed to simplify healthcare access by integrating intelligent symptom diagnosis, prescription understanding, appointment scheduling, hospital discovery, and patient engagement into a single application.

The platform combines state-of-the-art NLP models, OCR technologies, and cloud-based services to assist patients while reducing the workload on healthcare providers.

---

# 🚀 Key Features

## 🤖 AI Symptom Diagnosis

- Natural language symptom input
- Voice-based symptom reporting
- Biomedical Named Entity Recognition
- AI-generated diagnosis suggestions
- Medical literature validation
- Explainable AI reports

---

## 📄 Smart Prescription Reader

- Upload handwritten or printed prescriptions
- Dual OCR pipeline using EasyOCR + Tesseract
- Automatic medicine extraction
- Medicine information lookup
- Duplicate detection using fuzzy matching

---

## 📅 Appointment Management

- Book doctor appointments
- Manage appointment history
- Calendar integration
- Automated reminder scheduling

---

## 🔔 Smart Notifications

- SMS reminders via Twilio
- Firebase Push Notifications
- Background reminder scheduling using Celery

---

## 🏥 Hospital Finder

- Nearby hospital search
- OpenStreetMap integration
- Geolocation support
- Interactive map interface

---

## 🌍 Community Health Forum

- Create health discussions
- Upvote & downvote posts
- Threaded comments
- Category-based organization

---

## 🎙 Voice Assistant

- Speech-to-text symptom input
- Text-to-speech diagnosis summaries
- Hands-free interaction

---

# 🏗 System Architecture

```
                React Frontend
                       │
                  REST APIs
                       │
                Django Backend
       ┌───────────────┼───────────────┐
       │               │               │
 PostgreSQL       Redis + Celery     AI Layer
                                       │
          ┌────────────┬──────────────┬──────────────┐
          │            │              │              │
 Biomedical NER   Diagnosis AI   OCR Engine   Explainability
(HuggingFace)      (GPT-4o)    (EasyOCR + Tesseract)
```

---

# 🤖 AI Pipeline

### 1. Symptom Extraction

- HuggingFace Biomedical NER
- Compound symptom detection
- Severity extraction
- Entity confidence scoring

---

### 2. Diagnosis Generation

- GPT-4o (DxGPT)
- Clinical narrative generation
- Confidence scoring
- Local ML fallback model

---

### 3. Medical Validation

- Literature validation
- Case-study matching
- Evidence generation

---

### 4. Explainability

- AI-generated medical report
- Recommended precautions
- Diet suggestions
- Medication recommendations
- Voice-friendly summary

---

# 📄 Prescription OCR Pipeline

```
Prescription Image
        │
        ▼
 EasyOCR + Tesseract
        │
        ▼
 Text Extraction
        │
        ▼
 Medicine Detection
        │
        ▼
 Fuzzy Matching
        │
        ▼
 Medicine Database
        │
        ▼
 Structured Prescription
```

---

# ⚙ Tech Stack

## Frontend

- React
- Vite
- Axios
- React Router
- Context API

---

## Backend

- Django
- Django REST Framework
- JWT Authentication
- Google OAuth

---

## AI & Machine Learning

- HuggingFace Biomedical NER
- GPT-4o (DxGPT)
- EasyOCR
- Tesseract OCR
- Scikit-Learn

---

## Database

- PostgreSQL

---

## Background Services

- Celery
- Redis

---

## Notifications

- Twilio SMS
- Firebase Cloud Messaging

---

## Maps

- OpenStreetMap
- Nominatim API

---

## DevOps

- Docker
- Docker Compose

---

# 📂 Project Structure

```
DiagnoSure/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── api/
│   └── context/
│
├── backend/
│   ├── healthcare_backend/
│   ├── core/
│   ├── models/
│   ├── serializers/
│   ├── views/
│   └── tasks/
│
├── ai/
│   ├── symptom_parser/
│   ├── diagnosis/
│   ├── explainability/
│   ├── literature/
│   ├── case_studies/
│   └── prescription_reader/
│
├── docker/
│
└── README.md
```

---

# 🔄 Application Workflow

```
User Input (Text / Voice)
          │
          ▼
Symptom Extraction
          │
          ▼
Biomedical NER
          │
          ▼
AI Diagnosis Engine
          │
          ▼
Medical Validation
          │
          ▼
Explainability Report
          │
          ▼
Frontend Dashboard
```

---

# 🔐 Security Features

- JWT Authentication
- Google OAuth Login
- Role-Based Authorization
- Secure REST APIs
- CORS Protection
- Environment Variable Management
- Password Validation

---

# 📊 Core Modules

- AI Symptom Checker
- Smart Prescription Reader
- Appointment Scheduler
- Reminder Service
- Hospital Locator
- Community Forum
- Voice Assistant
- User Profile Management

---

# 📈 Scalability

The platform follows a modular architecture where:

- AI services can scale independently
- Celery workers process background jobs asynchronously
- Docker containers isolate services
- PostgreSQL provides reliable relational storage
- Redis manages asynchronous task queues

This architecture enables easy migration to cloud-native deployments using Kubernetes or managed cloud services.

---

# ✨ Highlights

- Multi-Agent AI Diagnosis Pipeline
- Biomedical Named Entity Recognition
- GPT-4o Assisted Diagnosis
- Explainable AI Reports
- Dual OCR Prescription Reader
- Voice-Based Healthcare Assistant
- Automated Appointment Reminders
- Hospital Discovery using Geolocation
- Community Healthcare Platform
- Dockerized Deployment

---

# 🚀 Future Enhancements

- Wearable Device Integration
- Electronic Health Record (EHR) Support
- Telemedicine Video Consultation
- AI Health Risk Prediction
- Multi-language Medical Assistant
- Personalized Healthcare Recommendations
- Medical Image Analysis
- Cloud Deployment on AWS/Azure

---

# 📸 Screenshots

Add screenshots of:

- Home Page
- AI Symptom Checker
- Prescription Reader
- Appointment Dashboard
- Hospital Map
- Community Forum
- User Profile

---

# 🛠 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/DiagnoSure.git
```

## Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Docker

```bash
docker-compose up --build
```

--

## ⭐ Support

If you found this project useful, please consider giving it a **Star ⭐** on GitHub.
