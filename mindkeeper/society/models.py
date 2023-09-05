from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=46, unique=True)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    is_private = models.BooleanField(default=False)
    is_receive_notifications = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)

    MAX_IMAGE_WIDTH = 600
    MAX_IMAGE_HEIGHT = 900

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'




