from django.contrib.auth import authenticate
from django.contrib.auth.forms import \
    UserCreationForm as DjangoUserCreationForm,\
    AuthenticationForm as DjangoAuthenticationForm

from django import forms

from django.core.exceptions import ValidationError
from .models import User
from email_app.tasks import send_verify_email


class UserCreationForm(DjangoUserCreationForm):

    username = forms.CharField(label='логин', widget=forms.TextInput(attrs={'class': 'form__input',
                                                                            'placeholder': 'Имя'}))
    password1 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form__input',
                                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form__input',
                                                                                  'placeholder': 'Пароль'}))
    email = forms.EmailField(label='почта', widget=forms.EmailInput(attrs={'class': 'form__input',                                                                'placeholder': ''}))
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'is_private', 'is_receive_notifications', 'image')


class AuthenticationForm(DjangoAuthenticationForm):
    username = forms.CharField(label='логин', widget=forms.TextInput(attrs={'class': 'form__input',
                                                                            'placeholder': 'Имя или почта'}))
    password = forms.CharField(label='пароль', widget=forms.PasswordInput(attrs={'class': 'form__input',
                                                                                  'placeholder': 'Пароль'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if not self.user_cache.is_email_verified:
                send_verify_email.delay(self.user_cache.pk)
                raise ValidationError('Почта не подтверждена')

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
