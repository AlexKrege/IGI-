# FROM python:3.11-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     libjpeg-dev \
#     zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Создаём папку для логов и медиа, чтобы избежать ошибок
# RUN mkdir -p logs media staticfiles

# ARG SECRET_KEY=django-insecure-build-key
# ARG DEBUG=False
# ARG ALLOWED_HOSTS="*"

# ENV SECRET_KEY=$SECRET_KEY \
#     DEBUG=$DEBUG \
#     ALLOWED_HOSTS=$ALLOWED_HOSTS

# # RUN python manage.py collectstatic --noinput

# EXPOSE 8000

# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libjpeg-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]