from datetime import datetime, timezone
from typing import List

from core.models.booking import LESSON_CHOICES_BOOKING_TIMES, Booking, Event, Weekday
from core.models.user import User
from core.serializers import BookingSerializer
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class BookingViewSet(viewsets.ModelViewSet):
    """
    Returns an booking given the id.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    http_method_names = ["get"]

    @extend_schema(
        request=BookingSerializer,
        responses={status.HTTP_201_CREATED: BookingSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID of the user for whom to create the booking.",
            )
        ],
    )
    @action(detail=False, methods=["get"])
    def get_user_bookings(self, request):
        id = int(request.query_params.get("id"))
        try:
            user = User.objects.get(id=id)
        except Exception:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        bookings = Booking.objects.filter(user=user)
        serialized_bookings = BookingSerializer(bookings, many=True).data
        return Response(serialized_bookings, status=status.HTTP_200_OK)


class CreateBookingView(ViewSet):
    @extend_schema(
        request=BookingSerializer,
        responses={status.HTTP_201_CREATED: BookingSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.QUERY,
                description="ID of the user for whom to create the booking.",
            )
        ],
    )
    @action(detail=False, methods=["post"])
    def create_booking(self, request):
        id = int(request.query_params.get("id"))
        try:
            user = User.objects.get(id=id)
        except Exception:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = dict(request.data)
        data["user"] = user.id
        lesson = data["lesson"]
        booking_time = datetime.fromisoformat(data["booking_time"])

        if booking_time < datetime.now(timezone.utc):
            return Response(data="booking time is less than todays date", status=status.HTTP_400_BAD_REQUEST)

        # Check if a booking already exists for the lesson and user
        lesson_choices = LESSON_CHOICES_BOOKING_TIMES[lesson]

        if lesson_choice_exists(lesson_choices, booking_time):
            existing_booking = Booking.objects.filter(user=user, lesson=lesson, booking_time=booking_time).first()
            if existing_booking:
                existing_booking.number_booked = Booking.objects.filter(
                    lesson=lesson, booking_time=booking_time
                ).count()
                existing_booking.save()
                return Response(BookingSerializer(existing_booking).data, status=status.HTTP_200_OK)

            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                booking = serializer.save()
                # Update all instances of Booking with the updated number of bookings
                Booking.objects.filter(lesson=lesson, booking_time=booking_time).update(
                    number_booked=Booking.objects.filter(lesson=data["lesson"], booking_time=booking_time).count()
                )
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        else:
            Response(data="class doesnt exist.", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def lesson_choice_exists(lesson_choices: List[Event], booking_time: datetime):
    weekday = booking_time.weekday()
    weekday = Weekday(weekday)

    for lesson in lesson_choices:
        if lesson.weekday == weekday and lesson.hour == booking_time.hour and lesson.minute == booking_time.minute:
            return True

    return False
