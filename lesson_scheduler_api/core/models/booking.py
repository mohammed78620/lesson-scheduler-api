from core.models.user import User
from django.db import models

LESSON_CHOICES = [
    ("wrestling", "Wrestling"),
    ("jui-jitsu", "Jui-jitsu"),
    ("boxing", "Boxing"),
]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_booked = models.IntegerField(default=0)
    size = models.IntegerField(default=30)
    lesson = models.CharField(max_length=20, choices=LESSON_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "booking"
