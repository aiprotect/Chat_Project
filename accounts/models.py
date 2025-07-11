from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import hashlib
# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(
        upload_to=''
        )
    phone_number = models.CharField(
        max_length = 20,
        verbose_name = 'شماره موبایل'

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), unique=True)


