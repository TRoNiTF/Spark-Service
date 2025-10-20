from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Service, Review, FAQ, CallRequest
from .forms import (
    CustomUserCreationForm, 
    CustomAuthenticationForm, 
    ProfileUpdateForm,
    ReviewForm,
    CallRequestForm
)


def home(request):
    """Главная страница"""
    return render(request, 'main/home.html')


def services(request):
    """Страница услуг"""
    services_list = Service.objects.all()
    return render(request, 'main/services.html', {'services': services_list})


def service_detail(request, service_id):
    """Детальная страница услуги"""
    service = get_object_or_404(Service, id=service_id)
    reviews = service.reviews.select_related('user').all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = service
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('service_detail', service_id=service.id)
    else:
        form = ReviewForm()
    
    return render(request, 'main/service_detail.html', {
        'service': service,
        'reviews': reviews,
        'form': form
    })


def contacts(request):
    """Страница контактов"""
    return render(request, 'main/contacts.html')


def about(request):
    """Страница о нас"""
    return render(request, 'main/about.html')


def faq(request):
    """Страница вопрос-ответ"""
    faq_list = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faq_list': faq_list})


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            # Показываем только первую ошибку
            for field in form:
                if field.errors:
                    for error in field.errors:
                        messages.error(request, f"{field.label}: {error}")
                        break
                    break
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'main/register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=telephone, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')
                return redirect('home')
        else:
            messages.error(request, 'Неверный номер телефона или пароль')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'main/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('home')


@login_required
def profile(request):
    """Страница профиля пользователя"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        
        # Обработка удаления изображения
        if 'delete_image' in request.POST:
            request.user.image.delete()
            request.user.save()
            messages.success(request, 'Изображение успешно удалено')
            return redirect('profile')
        
        # Обработка загрузки нового изображения
        if 'image' in request.FILES:
            request.user.image = request.FILES['image']
            request.user.save()
            messages.success(request, 'Изображение успешно обновлено')
            return redirect('profile')
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'main/profile.html', {'form': form})


@require_POST
def call_request(request):
    """Обработка заявки на звонок (AJAX)"""
    form = CallRequestForm(request.POST)
    
    if form.is_valid():
        call_req = form.save(commit=False)
        
        # Если указана услуга
        service_id = request.POST.get('service_id')
        if service_id:
            try:
                service = Service.objects.get(id=service_id)
                call_req.service = service
            except Service.DoesNotExist:
                pass
        
        call_req.save()
        
        # Отправка email
        subject = 'Новая заявка на звонок - Сервисный центр ИСКРА'
        message = f"""
        Новая заявка на звонок:
        
        Имя: {call_req.name}
        Телефон: {call_req.telephone}
        Услуга: {call_req.service.name if call_req.service else 'Не указана'}
        Дата: {call_req.created_at.strftime('%d.%m.%Y %H:%M')}
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['dim.shamaeff@yandex.ru'],
                fail_silently=True,
            )
        except:
            pass
        
        return JsonResponse({
            'success': True,
            'message': 'Заявка принята! Мы перезвоним вам в течение 15 минут.'
        })
    else:
        errors = []
        for field, error_list in form.errors.items():
            for error in error_list:
                errors.append(str(error))
        
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)


def privacy_policy(request):
    """Страница политики конфиденциальности"""
    return render(request, 'main/privacy_policy.html')

