from core.models import Booking, User
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            "Booking",
            summary="A booking object",
            description="A booking",
            value={
                "user": 30,
                "lesson": "wrestling",
            },
            request_only=False,
            response_only=True,
        ),
    ],
)
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["user", "lesson", "number_booked"]


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            "Count",
            summary="A count object.",
            description="A count object.",
            value={"count": 42},
            request_only=False,
            response_only=True,
        ),
    ],
)
class CountSerializer(serializers.Serializer):
    count = serializers.IntegerField()


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            "User",
            summary="A User object",
            description="A user",
            value={
                "username": "john@gmail.com",
                "password": "esgfwerf6er2as0",
            },
            request_only=True,
            response_only=False,
        ),
    ],
)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
