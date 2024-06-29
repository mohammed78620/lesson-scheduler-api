from datetime import date

from core.models import Booking, User
from dashboard.celery import app as celery_app
from dateutil.relativedelta import relativedelta
from django.db.models import Count


class UpdateUsersMissedBookings(celery_app.Task):
    name = "Update Missed Bookings"

    def run(self):
        today_date = date.today()
        bookings = Booking.objects.filter(
            expired_booking=False,
            attended=False,
            booking_time__date__lte=today_date,
            booking_time__date__gte=(today_date - relativedelta(months=1)),
        )

        if not bookings:
            return "no missed booking in the month."

        # set this column to true so the bookings doesnt get processed again
        bookings.update(expired_booking=True)

        users = bookings.values("user").annotate(num_bookings=Count("user"))

        for user in users:
            num_bookings = user["num_bookings"]
            user = User.objects.get(id=user["user"])
            user.missed_bookings += num_bookings
            user.save()

        return f"{len(users)} users have missed a booking."


celery_app.register_task(UpdateUsersMissedBookings())
