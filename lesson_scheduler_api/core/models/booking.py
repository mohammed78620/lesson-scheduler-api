from core.models.user import User
from django.db import models


class Booking(models.Model):
    # booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_booked = models.IntegerField(default=0)
    size = models.IntegerField(default=30)
    lesson = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "booking"
