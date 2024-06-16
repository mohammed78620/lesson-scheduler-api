from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    missed_bookings = models.IntegerField(default=0)

    class Meta:
        db_table = "user"
