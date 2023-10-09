from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.forms import UserCreationForm, AuthenticationForm
from users.models import User


class UserTestCase(TestCase):

    def test_user_reg(self):
        # Регистрация
        registration_url = reverse('users:registration')

        registration_form_data = UserCreationForm(data={
            'username': 'root123',
            'password1': '123321qqwweerr',
            'password2': '123321qqwweerr',
            'email': 'roottest123@gmail.com'
        }).data

        self.client.post(registration_url, data=registration_form_data)
        user = User.objects.last()
        self.assertIsNotNone(user, 'Пользователь не был зарегистрирован')

    def test_signin_without_verified_email(self):
        # Регистрация
        registration_url = reverse('users:registration')

        registration_form_data = UserCreationForm(data={
            'username': 'root123',
            'password1': '123321qqwweerr',
            'password2': '123321qqwweerr',
            'email': 'roottest123@gmail.com'
        }).data

        self.client.post(registration_url, data=registration_form_data)
        user = User.objects.last()
        self.assertIsNotNone(user, 'Пользователь не был зарегистрирован')

        # Проверка на возможность входа в аккаунт без верифицированной почты
        login_url = reverse('users:login')

        login_form_data = AuthenticationForm(data={
            'username': user.username,
            'password': '123321qqwweerr'
        }).data

        self.client.post(login_url, data=login_form_data)
        self.assertIsNone(user.last_login, msg='Пользователь смог войти без подтвержденной почты')

    def test_email_verify(self):
        # Регистрация пользователя
        registration_url = reverse('users:registration')

        registration_form_data = UserCreationForm(data={
            'username': 'root123',
            'password1': '123321qqwweerr',
            'password2': '123321qqwweerr',
            'email': 'roottest123@gmail.com'
        }).data

        self.client.post(registration_url, data=registration_form_data)
        user = User.objects.last()

        # Верифкация почты

        verify_url = reverse('users:verify_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })

        full_verify_url = f"http://127.0.0.1:8000{verify_url}"

        self.client.get(full_verify_url)
        user.refresh_from_db()

        self.assertTrue(user.is_email_verified, msg='Почта не подтвердилась')

    def test_signin_with_verified_email(self):
        # Регистрация пользователя
        registration_url = reverse('users:registration')

        registration_form_data = UserCreationForm(data={
            'username': 'root123',
            'password1': '123321qqwweerr',
            'password2': '123321qqwweerr',
            'email': 'roottest123@gmail.com'
        }).data

        self.client.post(registration_url, data=registration_form_data)
        user = User.objects.last()

        # Верифкация почты

        verify_url = reverse('users:verify_email', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })

        full_verify_url = f"http://127.0.0.1:8000{verify_url}"

        self.client.get(full_verify_url)
        user.refresh_from_db()

        login_url = reverse('users:login')

        login_form_data = AuthenticationForm(data={
            'username': user.username,
            'password': '123321qqwweerr'
        }).data

        self.client.post(login_url, data=login_form_data)
        self.assertIsNotNone(user.last_login, msg='Пользователь не смог войти с подтвержденной почтой')
