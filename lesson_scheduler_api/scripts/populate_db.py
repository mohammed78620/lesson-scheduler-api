import os
import random
import string
import sys

import django

# Add the project directory to the sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.settings")

# Configure Django
django.setup()

from core.models import Booking  # noqa: E402


def populate_database(num_entries):
    for _ in range(num_entries):
        # Generate a random ID
        booking_id = "".join(random.choices(string.ascii_letters + string.digits, k=10))

        # Create a Booking instance
        booking = Booking.objects.create(id=booking_id)

        # Set random values for number_booked and size
        booking.number_booked = random.randint(0, 50)
        booking.size = random.randint(10, 50)
        booking.save()

        print(f"Successfully created Booking instance with ID: {booking.id}")


if __name__ == "__main__":
    num_entries = 10  # Specify the desired number of entries
    populate_database(num_entries)
