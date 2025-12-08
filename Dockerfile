# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files
# and to ensure logs are output to the terminal in real-time
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (optional, but good for Postgres drivers later)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Run database migrations and then start the server
# Note: For high-traffic production, use 'gunicorn'. For MVP, runserver is fine.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
