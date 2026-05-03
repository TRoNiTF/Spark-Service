from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Service, Review, FAQ, CallRequest, CustomUser
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    ProfileUpdateForm,
    ReviewForm,
    CallRequestForm,
    PasswordChangeForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm
)
import secrets
from django.utils import timezone
from datetime import timedelta


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
    """Страница вопрос-ответ - фиксированные вопросы + из БД"""
    # Фиксированные вопросы (всегда отображаются)
    default_faqs = [
        {'question': 'Какие услуги вы предоставляете?',
         'answer': 'Мы предоставляем спектр услуг по ремонту электронных систем и дополнительного оборудования автомобилей, а также проводим инструментальную диагностику бензиновых двигателей.'},
        {'question': 'Сколько времени занимает ремонт?',
         'answer': 'Время ремонта зависит от сложности работ. Более сложный ремонт может занять от нескольких дней до недели. Точные сроки мы озвучиваем после диагностики.'},
        {'question': 'Какая гарантия на выполненные работы?',
         'answer': 'Мы предоставляем гарантию 14 дней на все виды работ.'},
        {'question': 'Нужно ли записываться заранее?',
         'answer': 'Мы рекомендуем записываться заранее, чтобы мы могли зарезервировать для вас время. Однако мы также принимаем клиентов без записи по мере возможности.'},
        {'question': 'Какие формы оплаты вы принимаете?',
         'answer': 'Мы принимаем оплату наличными и безналичным расчетом по договору.'},
    ]

    # Вопросы из базы данных
    db_faqs = FAQ.objects.all().order_by('order', 'id')

    # Объединяем: сначала фиксированные, потом из БД
    all_faqs = default_faqs + list(db_faqs)

    return render(request, 'main/faq.html', {'faq_list': all_faqs})


def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Указываем бэкенд для входа
            user.backend = 'main.backends.PhoneBackend'
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
    message = None

    # Обработка обновления профиля (имя, фамилия, отчество, дата, телефон, email)
    if 'update_profile' in request.POST:
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')

    # Обработка смены пароля
    elif 'change_password' in request.POST:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password1')
            request.user.set_password(new_password)
            request.user.save()
            # Обновляем сессию, чтобы пользователь не вышел
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    # Обработка удаления изображения
    elif 'delete_image' in request.POST:
        if request.user.image:
            request.user.image.delete()
            request.user.save()
            messages.success(request, 'Изображение успешно удалено')
            return redirect('profile')

    # Обработка загрузки нового изображения
    elif 'image' in request.FILES:
        request.user.image = request.FILES['image']
        request.user.save()
        messages.success(request, 'Изображение успешно обновлено')
        return redirect('profile')

    profile_form = ProfileUpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)

    return render(request, 'main/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'user': request.user
    })


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

        # Отправка email на почту администратора
        subject = 'Новая заявка на звонок - Сервисный центр «ИСКРА»'
        message = f"""
        Здравствуйте!

        Поступила новая заявка на звонок:

        ┌─────────────────────────────────────┐
        │ Имя: {call_req.name}
        │ Телефон: {call_req.telephone}
        │ Услуга: {call_req.service.name if call_req.service else 'Не указана'}
        │ Дата и время: {call_req.created_at.strftime('%d.%m.%Y %H:%M')}
        └─────────────────────────────────────┘

        Свяжитесь с клиентом в ближайшее время.

        ---
        Сервисный центр «ИСКРА»
        """

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  # Отправляем на почту из настроек
                fail_silently=False,
            )
        except Exception as e:
            print(f'Ошибка отправки email: {e}')

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


reset_tokens = {}


def password_reset_request(request):
    """Запрос на восстановление пароля - ввод email"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.get(email=email)

            # Генерируем токен
            token = secrets.token_urlsafe(32)
            reset_tokens[token] = {
                'user_id': user.id,
                'expires_at': timezone.now() + timedelta(minutes=5)
            }

            # Отправляем письмо
            reset_url = request.build_absolute_uri(f'/password-reset-confirm/{token}/')

            subject = 'Восстановление пароля - Сервисный центр «ИСКРА»'
            message = f"""
            Здравствуйте, {user.get_full_name()}!

            Вы запросили восстановление пароля на сайте Сервисный центр «ИСКРА».

            Для установки нового пароля перейдите по ссылке:
            {reset_url}

            Ссылка действительна в течение 5 минут.

            Если вы не запрашивали восстановление пароля, проигнорируйте это письмо.

            С уважением,
            Сервисный центр «ИСКРА»
            """

            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Письмо с инструкцией отправлено на ваш email')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Ошибка при отправке письма. Попробуйте позже.')
                return redirect('password_reset_request')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'main/password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """Подтверждение сброса пароля - ввод нового пароля"""
    # Проверяем токен
    token_data = reset_tokens.get(token)
    if not token_data:
        messages.error(request, 'Ссылка недействительна или устарела')
        return redirect('password_reset_request')

    if timezone.now() > token_data['expires_at']:
        del reset_tokens[token]
        messages.error(request, 'Срок действия ссылки истёк (5 минут)')
        return redirect('password_reset_request')

    user_id = token_data['user_id']
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()

            # Удаляем использованный токен
            del reset_tokens[token]

            # Указываем бэкенд для входа (ВАЖНО!)
            user.backend = 'main.backends.PhoneBackend'
            login(request, user)
            messages.success(request, 'Пароль успешно изменён!')
            return redirect('profile')
    else:
        form = PasswordResetConfirmForm()

    return render(request, 'main/password_reset_confirm.html', {'form': form, 'token': token})