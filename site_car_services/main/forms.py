from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Review, CallRequest
import re
from datetime import date


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя'
        }),
        label='Имя'
    )
    surname = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия'
        }),
        label='Фамилия'
    )
    patronymic = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Отчество (при наличии)'
        }),
        label='Отчество'
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Дата рождения'
        }),
        label='Дата рождения'
    )
    telephone = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (___) ___ - __ - __',
            'id': 'phone-input'
        }),
        label='Телефон'
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/gif,image/webp'
        }),
        label='Фото профиля'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'password1'
        }),
        label='Пароль',
        help_text='8-15 символов, заглавная буква, латиница, цифра'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'id': 'password2'
        }),
        label='Подтверждение пароля'
    )
    agree_privacy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Согласен с политикой обработки персональных данных'
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'patronymic', 'birth_date', 'telephone', 'image', 'password1', 'password2')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$', name):
            raise ValidationError('Имя должно начинаться с заглавной буквы и содержать только русские буквы')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$', surname):
            raise ValidationError('Фамилия должна начинаться с заглавной буквы и содержать только русские буквы')
        return surname

    def clean_patronymic(self):
        patronymic = self.cleaned_data.get('patronymic')
        if patronymic and not re.match(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$', patronymic):
            raise ValidationError('Отчество должно начинаться с заглавной буквы и содержать только русские буквы')
        return patronymic

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            if birth_date.year < 1910:
                raise ValidationError('Дата рождения не может быть раньше 1910 года')
            if birth_date > date.today():
                raise ValidationError('Дата рождения не может быть в будущем')
        return birth_date

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        # Убираем все символы кроме цифр
        telephone_digits = re.sub(r'\D', '', telephone)

        # Проверяем формат
        if not re.match(r'^7\d{10}$', telephone_digits):
            raise ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')

        # Форматируем для сохранения
        formatted = '+' + telephone_digits

        # Проверяем уникальность
        if CustomUser.objects.filter(telephone=formatted).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует')

        return formatted

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8 or len(password) > 15:
            raise ValidationError('Пароль должен быть от 8 до 15 символов')

        if not re.search(r'[A-Z]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')

        if not re.search(r'[a-z]', password):
            raise ValidationError('Пароль должен содержать латинские буквы')

        if not re.search(r'\d', password):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')

        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError('Пароль должен содержать только латинские буквы и цифры')

        return password

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер изображения не должен превышать 5 МБ')

            allowed_formats = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if image.content_type not in allowed_formats:
                raise ValidationError('Допустимые форматы: JPG, PNG, GIF, WEBP')
        return image


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (___) ___ - __ - __',
            'id': 'login-phone-input'
        }),
        label='Телефон'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'login-password'
        }),
        label='Пароль'
    )


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    surname = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    patronymic = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Отчество'
    )
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Дата рождения'
    )
    telephone = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'profile-phone-input'
        }),
        label='Телефон'
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'patronymic', 'birth_date', 'telephone')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$', name):
            raise ValidationError('Имя должно начинаться с заглавной буквы и содержать только русские буквы')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$', surname):
            raise ValidationError('Фамилия должна начинаться с заглавной буквы и содержать только русские буквы')
        return surname


class ReviewForm(forms.ModelForm):
    description = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Напишите ваш отзыв...'
        }),
        label='Отзыв'
    )

    class Meta:
        model = Review
        fields = ('description',)


class CallRequestForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        }),
        label='Имя'
    )
    telephone = forms.CharField(
        max_length=18,
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-input',
            'placeholder': '+7 (___) ___ - __ - __'
        }),
        label='Телефон'
    )
    agree_privacy = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Согласен с политикой обработки персональных данных'
    )

    class Meta:
        model = CallRequest
        fields = ('name', 'telephone')

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        telephone_digits = re.sub(r'\D', '', telephone)

        if not re.match(r'^7\d{10}$', telephone_digits):
            raise ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')

        return '+' + telephone_digits