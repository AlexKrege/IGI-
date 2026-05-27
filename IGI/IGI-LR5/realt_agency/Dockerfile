FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости для Pillow и Matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Определяем переменные для этапа сборки (build args)
# Они не сохраняются в финальном образе, но нужны для collectstatic
ARG SECRET_KEY=django-insecure-build-key
ARG DEBUG=False
ARG ALLOWED_HOSTS="*"

# Передаём их в окружение на время выполнения команды сборки
ENV SECRET_KEY=$SECRET_KEY \
    DEBUG=$DEBUG \
    ALLOWED_HOSTS=$ALLOWED_HOSTS

# Собираем статику
RUN python manage.py collectstatic --noinput

# Очищаем кэш pip (экономит место)
RUN rm -rf /root/.cache/pip

# Открываем порт
EXPOSE 8000

# Запускаем сервер через gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]