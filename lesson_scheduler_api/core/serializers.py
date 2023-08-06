from core.models import Booking
from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

User = get_user_model()


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
        fields = ("id", "username", "email")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials Passed.")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], validated_data["email"], validated_data["password"]
        )
        return user
