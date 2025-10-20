#!/bin/bash

# Скрипт быстрой настройки проекта

echo "🚀 Настройка проекта Сервисный центр ИСКРА"
echo "==========================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 не найден. Установите Python 3.11 или выше."
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание директорий
echo "📁 Создание необходимых директорий..."
mkdir -p media/profile_images
mkdir -p media/service_images
mkdir -p staticfiles

# Применение миграций
echo "🗄️  Применение миграций базы данных..."
python manage.py makemigrations
python manage.py migrate

# Создание суперпользователя
echo ""
echo "👤 Создание суперпользователя (администратора)"
echo "Введите данные для входа в админ-панель:"
python manage.py createsuperuser

# Сбор статических файлов
echo ""
echo "📦 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Настройка завершена!"
echo ""
echo "Для запуска сервера выполните:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Сайт будет доступен по адресу: http://127.0.0.1:8000/"
echo "Админ-панель: http://127.0.0.1:8000/admin/"
echo ""

