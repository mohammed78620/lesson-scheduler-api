from core.models import Booking, User
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
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        data["user"] = user.id

        # Check if a booking already exists for the lesson and user
        existing_booking = Booking.objects.filter(user=user, lesson=data["lesson"]).first()
        if existing_booking:
            existing_booking.number_booked = Booking.objects.filter(lesson=data["lesson"]).count()
            existing_booking.save()
            return Response(BookingSerializer(existing_booking).data, status=status.HTTP_200_OK)

        serializer = BookingSerializer(data=data)
        if serializer.is_valid():
            booking = serializer.save()
            # Update all instances of Booking with the updated number of bookings
            Booking.objects.filter(lesson=data["lesson"]).update(
                number_booked=Booking.objects.filter(lesson=data["lesson"]).count()
            )
            return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
