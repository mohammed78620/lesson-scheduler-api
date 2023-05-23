from core.models.booking import Booking
from core.serializers import BookingSerializer, CountSerializer
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema

# from core.serializers import
from rest_framework import mixins, viewsets
from rest_framework.decorators import action


class BookingViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Returns an booking given the id.
    """

    serializer_class = BookingSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Booking.objects.all()

    @extend_schema(
        responses={200: CountSerializer()},
    )
    @action(detail=False, methods=["get"], filter_backends=[])
    def metrics(self, request):
        """
        Returns the number of edges in the database.
        """
        a = Booking.objects.all().count()
        return JsonResponse({"count": a})
