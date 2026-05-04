from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            return None

        # Очищаем телефон от всех нецифровых символов
        clean_phone = ''.join(filter(str.isdigit, username))

        # Если длина 11 и начинается с 8, меняем на +7
        if len(clean_phone) == 11 and clean_phone.startswith('8'):
            clean_phone = '+7' + clean_phone[1:]
        elif len(clean_phone) == 11 and clean_phone.startswith('7'):
            clean_phone = '+' + clean_phone

        try:
            user = User.objects.get(telephone=clean_phone)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None