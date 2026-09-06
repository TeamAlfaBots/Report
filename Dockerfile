# 1. Base Image: Python ka lightweight version use karein
FROM python:3.9-slim

# 2. Environment Variables: Python ke liye optimization
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Working Directory: Container ke andar folder set karein
WORKDIR /app

# 4. System Dependencies: Build tools install karein
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 5. Requirements: Sabse pehle dependencies copy karke install karein
# Isse Docker layer caching mein madad milti hai
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Project Files: Poora project code container mein copy karein
COPY . .

# 7. Port: Web server (FastAPI) ke liye port expose karein
# Ye wahi port hai jise UptimeRobot ping karega
EXPOSE 8080

# 8. Run Command: Bot aur Web Server shuru karne ke liye
# Hum main.py chalayenge jo internally threading se sab handle karega
CMD ["python", "main.py"]
