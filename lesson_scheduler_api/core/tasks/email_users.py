import smtplib
from email.message import EmailMessage

from core.email_message import generate_email_body
from core.models import User
from dashboard.celery import app as celery_app
from dashboard.settings import GOOGLE_APP_PASSWORD, MAXIMUM_NUMBER_OF_MISSED_BOOKINGS, SENDER_EMAIL_ADDRESS


class EmailUsers(celery_app.Task):
    """
    The tasks gets users where the number of missed bookings are exceeded, sends them a email
    and resets the number of missed bookings.
    """

    name = "Email Users"

    def run(self):
        users = User.objects.filter(missed_bookings__gte=MAXIMUM_NUMBER_OF_MISSED_BOOKINGS)

        if not users:
            return f"no users missed more than {MAXIMUM_NUMBER_OF_MISSED_BOOKINGS}."

        msg = EmailMessage()
        msg["Subject"] = "Notice: Missed Bookings"
        msg["From"] = SENDER_EMAIL_ADDRESS

        # with smtplib.SMTP("localhost", 1025) as smtp:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL_ADDRESS, GOOGLE_APP_PASSWORD)
            for user in users.iterator():
                msg["To"] = user.email
                full_name = user.get_full_name()
                body = generate_email_body(full_name, user.missed_bookings)
                msg.set_content(body)

            smtp.send_message(msg)

            user.missed_bookings = 0
            user.save()

        return f"Emailed {len(users)} user."


celery_app.register_task(EmailUsers())
