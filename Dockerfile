# Dockerfile for Oracle Cloud / Railway deployment
FROM python:3.11-slim

# Sistem güncellemeleri ve gerekli paketler
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Çalışma dizini
WORKDIR /app

# Python requirements
COPY requirements_flask.txt .
RUN pip install --no-cache-dir -r requirements_flask.txt

# Uygulama dosyalarını kopyala
COPY app_flask.py .

# Port açma
EXPOSE 5000

# Uygulama başlatma
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "60", "app_flask:app"]
