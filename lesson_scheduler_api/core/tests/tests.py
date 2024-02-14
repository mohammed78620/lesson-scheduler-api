import json

from core.models import Booking
from core.views import CreateBookingView, SignInAPI, SignUpAPI
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

User = get_user_model()


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


class SignUpAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SignUpAPI.as_view({"post": "signup"})
        self.user_data = {"username": "lZQ@OhYTpjwVAs-zljkEJ", "email": "user@example.com", "password": "string"}

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_sign_up(self):
        url = "/user/signup/"

        request = self.factory.post(url, data=json.dumps(self.user_data), content_type="application/json")
        request.META["HTTP_ACCEPT"] = self.headers["accept"]
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().get_username(), self.user_data["username"])


class SignInAPITestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SignInAPI.as_view({"post": "signin"})
        self.user_data = {"username": "testuser", "password": "testpassword"}
        self.user = User.objects.create_user(**self.user_data)
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_sign_in(self):
        url = "/user/signin/"

        request = self.factory.post(url, data=json.dumps(self.user_data), content_type="application/json")
        request.META["HTTP_ACCEPT"] = self.headers["accept"]
        force_authenticate(request, user=self.user)
        response = self.view(request)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.first().get_username(), self.user_data["username"])
