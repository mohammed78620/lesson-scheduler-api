import json

from core.models import Booking, User
from core.views import CreateBookingView
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class CreateBookingViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateBookingView.as_view({"post": "create_booking"})
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.booking_data = {"lesson": "wrestling"}
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_create_booking(self):
        url = "/core/create_booking/?id={}".format(self.user.id)

        request = self.factory.post(url, data=json.dumps(self.booking_data), content_type="application/json")
        request.META["HTTP_ACCEPT"] = self.headers["accept"]
        force_authenticate(request, user=self.user)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)
        self.assertEqual(Booking.objects.first().lesson, self.booking_data["lesson"])
