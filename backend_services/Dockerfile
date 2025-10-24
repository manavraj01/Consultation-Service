# backend_services/Dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port
EXPOSE 8000

# Run migrations & start server
CMD ["sh", "-c", "python telemed/manage.py makemigrations &&  python telemed/manage.py migrate && python telemed/manage.py loaddata data_generation/seed_data.json && python telemed/manage.py runserver 0.0.0.0:8000"]
