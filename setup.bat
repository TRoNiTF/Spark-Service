@echo off
chcp 65001 > nul

echo 🚀 Настройка проекта Сервисный центр ИСКРА
echo ===========================================
echo.

REM Проверка Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Установите Python 3.11 или выше.
    pause
    exit /b 1
)

python --version
echo.

REM Создание виртуального окружения
echo 📦 Создание виртуального окружения...
python -m venv venv

REM Активация виртуального окружения
echo 🔄 Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка зависимостей
echo 📥 Установка зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Создание директорий
echo 📁 Создание необходимых директорий...
if not exist "media\profile_images" mkdir media\profile_images
if not exist "media\service_images" mkdir media\service_images
if not exist "staticfiles" mkdir staticfiles

REM Применение миграций
echo 🗄️  Применение миграций базы данных...
python manage.py makemigrations
python manage.py migrate

REM Создание суперпользователя
echo.
echo 👤 Создание суперпользователя (администратора)
echo Введите данные для входа в админ-панель:
python manage.py createsuperuser

REM Сбор статических файлов
echo.
echo 📦 Сбор статических файлов...
python manage.py collectstatic --noinput

echo.
echo ✅ Настройка завершена!
echo.
echo Для запуска сервера выполните:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Сайт будет доступен по адресу: http://127.0.0.1:8000/
echo Админ-панель: http://127.0.0.1:8000/admin/
echo.
pause

