#!/usr/bin/env bash
set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

echo "🌱 Seeding demo data..."
python manage.py seed_data

echo "✅ Build tasks completed!"
