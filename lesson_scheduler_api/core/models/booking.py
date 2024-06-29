from dataclasses import dataclass
from enum import Enum

from core.models.user import User
from django.db import models


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


@dataclass
class Event:
    name: str
    weekday: int
    hour: int
    minute: int


LESSON_CHOICES = [
    ("wrestling", "Wrestling"),
    ("jui-jitsu", "Jui-jitsu"),
    ("boxing", "Boxing"),
]

LESSON_CHOICES_BOOKING_TIMES = {
    "wrestling": [Event("wrestling", Weekday.MONDAY, 13, 0), Event("wrestling", Weekday.TUESDAY, 14, 0)],
    "jui-jtisu": [Event("jui-jtisu", Weekday.WEDNESDAY, 14, 30), Event("jui-jtisu", Weekday.THURSDAY, 14, 0)],
    "boxing": [Event("boxing", Weekday.FRIDAY, 14, 0)],
}

BOOKING_LIMIT = 30


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_booked = models.IntegerField(default=0)
    size = models.IntegerField(default=30)
    lesson = models.CharField(max_length=20, choices=LESSON_CHOICES)
    time_booked = models.DateTimeField(auto_now_add=True)
    booking_time = models.DateTimeField()
    attended = models.BooleanField(default=False)
    expired_booking = models.BooleanField(default=False)

    class Meta:
        db_table = "booking"
