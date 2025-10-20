from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
import re


class CustomUserManager(BaseUserManager):
    def create_user(self, telephone, password=None, **extra_fields):
        if not telephone:
            raise ValueError('Номер телефона обязателен')
        user = self.model(telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telephone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    telephone_validator = RegexValidator(
        regex=r'^\+?7\d{10}$',
        message='Номер телефона должен быть в формате: +79991234567'
    )
    
    name = models.CharField('Имя', max_length=20)
    surname = models.CharField('Фамилия', max_length=20)
    patronymic = models.CharField('Отчество', max_length=20, blank=True, null=True)
    telephone = models.CharField('Телефон', max_length=12, unique=True, validators=[telephone_validator])
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    image = models.ImageField('Фото профиля', upload_to='profile_images/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['name', 'surname']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'
    
    def __str__(self):
        return f"{self.surname} {self.name} ({self.telephone})"
    
    def get_full_name(self):
        if self.patronymic:
            return f"{self.surname} {self.name} {self.patronymic}"
        return f"{self.surname} {self.name}"


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=60)
    description = models.TextField('Описание', max_length=255)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='service_images/')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        db_table = 'services'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='reviews')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Услуга', related_name='reviews')
    description = models.TextField('Текст отзыва', max_length=255)
    date = models.DateField('Дата отзыва', auto_now_add=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        db_table = 'reviews'
        ordering = ['-date']
    
    def __str__(self):
        return f"Отзыв от {self.user.get_full_name()} на {self.service.name}"


class CallRequest(models.Model):
    name = models.CharField('Имя', max_length=50)
    telephone = models.CharField('Телефон', max_length=20)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Услуга')
    message = models.TextField('Сообщение', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        verbose_name = 'Заявка на звонок'
        verbose_name_plural = 'Заявки на звонок'
        db_table = 'call_requests'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заявка от {self.name} ({self.telephone})"


class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    order = models.IntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Вопрос-Ответ'
        verbose_name_plural = 'Вопросы-Ответы'
        db_table = 'faq'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.question

