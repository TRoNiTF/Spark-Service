# 🚀 Развертывание в продакшене

## Подготовка к развертыванию

### 1. Настройки безопасности

Отредактируйте `iskra/settings.py`:

```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ваш-очень-секретный-ключ-который-никто-не-знает'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-ip-address']

# CSRF settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

### 2. База данных (PostgreSQL рекомендуется)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iskra_db',
        'USER': 'iskra_user',
        'PASSWORD': 'strong_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Установите зависимость:
```bash
pip install psycopg2-binary
```

### 3. Email настройки

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dim.shamaeff@yandex.ru'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')  # Используйте переменные окружения!
```

### 4. Статические файлы

```python
STATIC_ROOT = '/var/www/iskra/static/'
MEDIA_ROOT = '/var/www/iskra/media/'
```

## Развертывание с Gunicorn + Nginx

### 1. Установка зависимостей

```bash
pip install gunicorn
pip install psycopg2-binary
```

Обновите `requirements.txt`:
```txt
Django==5.1
Pillow==10.4.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 2. Создание Gunicorn сервиса

Создайте файл `/etc/systemd/system/iskra.service`:

```ini
[Unit]
Description=Iskra Service Center Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/iskra
Environment="PATH=/var/www/iskra/venv/bin"
ExecStart=/var/www/iskra/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/iskra/iskra.sock \
    iskra.wsgi:application

[Install]
WantedBy=multi-user.target
```

Запустите сервис:
```bash
sudo systemctl start iskra
sudo systemctl enable iskra
```

### 3. Настройка Nginx

Создайте файл `/etc/nginx/sites-available/iskra`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/iskra/staticfiles/;
    }

    location /media/ {
        alias /var/www/iskra/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/iskra/iskra.sock;
    }
}
```

Активируйте конфигурацию:
```bash
sudo ln -s /etc/nginx/sites-available/iskra /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. SSL сертификат (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Развертывание на VPS

### Пошаговая инструкция

#### 1. Подключение к серверу

```bash
ssh root@your-server-ip
```

#### 2. Обновление системы

```bash
apt update && apt upgrade -y
```

#### 3. Установка зависимостей

```bash
apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib -y
```

#### 4. Создание пользователя

```bash
adduser iskra
usermod -aG sudo iskra
su - iskra
```

#### 5. Клонирование проекта

```bash
cd /var/www
sudo mkdir iskra
sudo chown iskra:iskra iskra
cd iskra
git clone <your-repo-url> .
```

#### 6. Настройка виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 7. Настройка PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE iskra_db;
CREATE USER iskra_user WITH PASSWORD 'strong_password';
ALTER ROLE iskra_user SET client_encoding TO 'utf8';
ALTER ROLE iskra_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE iskra_user SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE iskra_db TO iskra_user;
\q
```

#### 8. Миграции и статика

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

#### 9. Настройка прав доступа

```bash
sudo chown -R www-data:www-data /var/www/iskra
sudo chmod -R 755 /var/www/iskra
```

## Развертывание на Docker (опционально)

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "iskra.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=iskra_db
      - POSTGRES_USER=iskra_user
      - POSTGRES_PASSWORD=strong_password

  web:
    build: .
    command: gunicorn iskra.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://iskra_user:strong_password@db:5432/iskra_db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

Запуск:
```bash
docker-compose up -d
```

## Мониторинг и обслуживание

### Логи

```bash
# Gunicorn логи
sudo journalctl -u iskra

# Nginx логи
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Резервное копирование

```bash
# База данных
pg_dump iskra_db > backup_$(date +%Y%m%d).sql

# Медиа файлы
tar -czf media_backup_$(date +%Y%m%d).tar.gz /var/www/iskra/media/
```

### Обновление проекта

```bash
cd /var/www/iskra
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart iskra
```

## Checklist перед запуском

- [ ] DEBUG = False
- [ ] SECRET_KEY изменен на безопасный
- [ ] ALLOWED_HOSTS настроен
- [ ] База данных PostgreSQL настроена
- [ ] Email настроен с паролем приложения
- [ ] SSL сертификат установлен
- [ ] Статические файлы собраны
- [ ] Медиа директория с правильными правами
- [ ] Резервное копирование настроено
- [ ] Мониторинг настроен
- [ ] Firewall настроен (порты 80, 443)

## Производительность

### Оптимизация Django

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Сжатие
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... остальные middleware
]
```

### Оптимизация Nginx

```nginx
# Кэширование статики
location /static/ {
    alias /var/www/iskra/staticfiles/;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Gzip сжатие
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

---

**Удачного развертывания! 🚀**

