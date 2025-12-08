📖 Bible Quiz MVP

A full-stack, gamified scripture learning application built with Django 5+ and Django REST Framework.

This project delivers a fast, interactive Bible quiz experience featuring daily challenges, progress tracking, streaks, and community leaderboards. It includes a decoupled API backend and a responsive Tailwind CSS frontend.

🚀 Features

🔥 Core Experience

Daily Random Quiz: A unique set of 7 questions generated every 24 hours, cached globally for all users to ensure a shared community experience.

Category Packs: Focused quizzes on specific topics (e.g., Guess the Verse, Who Said This?, Old vs New Testament).

Gamified Learning: Instant feedback on answers to aid memorization.

📈 Engagement Engines

Progress Tracking: Tracks total score, quizzes played, and average accuracy anonymously via Device ID.

Daily Streaks: Smart logic that tracks consecutive days played (yesterday vs. today).

Real-Time Leaderboard: Aggregates user scores dynamically. Supports filtering by Church/Group ID for local community competitions.

🛠 Technical Highlights

REST API: Fully documented endpoints using Swagger/OpenAPI.

Caching: Redis-ready caching layer (using LocMemCache for MVP) for the Daily Quiz lock.

Dockerized: One-command deployment setup.

Responsive UI: Built with Django Templates and Tailwind CSS.

🏗 Tech Stack

Backend: Python 3.11, Django 5.0, Django REST Framework

Database: SQLite (MVP) / PostgreSQL (Production ready via settings)

Frontend: Django Templates, Tailwind CSS (CDN), Vanilla JS

Documentation: drf-spectacular (Swagger UI)

Containerization: Docker & Docker Compose

⚡ Getting Started (Local Development)

Follow these steps to run the project manually on your machine.

1. Clone & Setup

# Clone the repository
git clone [https://github.com/your-username/bible-quiz-mvp.git](https://github.com/your-username/bible-quiz-mvp.git)
cd bible-quiz-mvp

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt


2. Environment Configuration

Create a .env file in the root directory:

SECRET_KEY=django-insecure-dev-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
# Leave DB_NAME empty to use SQLite by default


3. Database & Seeding

# Run migrations to create database tables
python manage.py makemigrations quiz_api
python manage.py migrate

# Seed the database with initial questions and categories
python manage.py seed_data


4. Run the Server

python manage.py runserver


Frontend: https://www.google.com/search?q=http://127.0.0.1:8000/

API Docs: https://www.google.com/search?q=http://127.0.0.1:8000/api/docs/

🐳 Getting Started (Docker)

Run the entire application in an isolated container.

# Build and start the container
docker-compose up --build


The app will be available at http://localhost:8000.

📚 API Documentation

The API is self-documenting. Once the server is running, visit:
http://127.0.0.1:8000/api/docs/

Key Endpoints

Method

Endpoint

Description

GET

/api/daily-quiz/

Get today's locked random questions

POST

/api/submit-answers/

Submit answers, get score, update streak

GET

/api/stats/?device_id=...

Get user progress and streaks

GET

/api/leaderboard/

Global top 10 rankings

GET

/api/leaderboard/?group_id=...

Filter leaderboard by Church Group

📂 Project Structure

bible_quiz_project/
├── manage.py              # Django CLI utility
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (GitIgnored)
│
├── bible_quiz_project/    # Project Settings
│   ├── settings.py
│   └── urls.py
│
├── quiz_api/              # Backend Application
│   ├── models.py          # Database Schema (Questions, Attempts)
│   ├── views.py           # API Logic (Quizzes, Streaks, Leaderboard)
│   ├── serializers.py     # JSON Formatting
│   ├── admin.py           # Admin Panel Config
│   └── management/commands/seed_data.py  # Seeding Script
│
└── quiz_ui/               # Frontend Application
    ├── templates/quiz_ui/ # HTML Files (Home, Quiz, Leaderboard)
    └── views.py           # Template Views


🧪 Running Tests

Verify the Daily Quiz locking mechanism and scoring logic:

python manage.py test quiz_api


🔮 Future Roadmap

[ ] Add PostgreSQL for production database.

[ ] Implement Authentication (optional) for cross-device syncing.

[ ] Add "Verse of the Day" push notifications (Frontend PWA).

[ ] Create an