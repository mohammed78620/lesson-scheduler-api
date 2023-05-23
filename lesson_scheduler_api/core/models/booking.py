from django.db import models


class Booking(models.Model):
    id = models.TextField(primary_key=True)
    number_booked = models.IntegerField(default=0)
    size = models.IntegerField(default=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "booking"
