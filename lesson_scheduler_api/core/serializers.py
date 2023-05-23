from core.models.booking import Booking
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers


@extend_schema_serializer(
    many=True,
    examples=[
        OpenApiExample(
            "Booking",
            summary="A booking object",
            description="A booking",
            value={"id": "1", "number_booked": 1, "size": 30},
            request_only=False,
            response_only=True,
        ),
    ],
)
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "number_booked",
            "size",
        )
        depth = 1


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
