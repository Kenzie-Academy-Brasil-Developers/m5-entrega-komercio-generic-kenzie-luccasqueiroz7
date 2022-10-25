from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False,
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(
        null=True,
        blank=True,
        default=False,
    )
