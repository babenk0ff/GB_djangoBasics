from pathlib import Path
from time import time

from django.contrib.auth.models import AbstractUser
from django.db import models

from mainapp.models import NULLABLE


def users_avatars_path(instance, filename):
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return "user_{0}/avatars/{1}".format(instance.username, f"pic_{num}{suff}")


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name='Email', unique=True)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', **NULLABLE)
    avatar = models.ImageField(upload_to=users_avatars_path, **NULLABLE)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
