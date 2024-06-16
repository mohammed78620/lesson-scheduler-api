import smtplib
from datetime import date
from email.message import EmailMessage

from celery.utils.log import get_task_logger
from core.email_message import generate_email_body
from core.models import Booking, User
from dashboard.celery import app as celery_app
from dashboard.settings import GOOGLE_APP_PASSWORD, MAXIMUM_NUMBER_OF_MISSED_BOOKINGS
from dateutil.relativedelta import relativedelta
from django.db.models import Count

logger = get_task_logger(__name__)


class ExampleTask(celery_app.Task):
    name = "Example Task"

    def run(self):
        return "this is a example task"


class UpdateUsersMissedBookings(celery_app.Task):
    name = "Update Missed Bookings"

    def run(self):
        today_date = date.today()
        bookings = Booking.objects.filter(
            attended=False,
            booking_time__date__lte=today_date,
            booking_time__date__gte=(today_date - relativedelta(months=1)),
        )

        if not bookings:
            return "no missed booking in the month."

        users = bookings.values("user").annotate(num_bookings=Count("user"))

        for user in users:
            num_bookings = user["num_bookings"]
            user = User.objects.get(id=user["user"])
            user.missed_bookings += num_bookings
            user.save()

        return f"{len(users)} users have missed a booking."


class EmailUsers(celery_app.Task):
    name = "Email Users"

    def run(self):
        users = User.objects.filter(missed_bookings__gte=MAXIMUM_NUMBER_OF_MISSED_BOOKINGS)

        if not users:
            return f"no users missed more than {MAXIMUM_NUMBER_OF_MISSED_BOOKINGS}."

        EMAIL_ADDRESS = "mohammedmiah786984321234@gmail.com"
        msg = EmailMessage()
        msg["Subject"] = "Notice: Missed Bookings"
        msg["From"] = EMAIL_ADDRESS

        # with smtplib.SMTP("localhost", 1025) as smtp:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, GOOGLE_APP_PASSWORD)
            for user in users.iterator():
                msg["To"] = user.email
                full_name = user.get_full_name()
                body = generate_email_body(full_name, user.missed_bookings)
                msg.set_content(body)

            smtp.send_message(msg)

        return f"Emailed {len(users)} user."


celery_app.register_task(UpdateUsersMissedBookings())
celery_app.register_task(EmailUsers())
