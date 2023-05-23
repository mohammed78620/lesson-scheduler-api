from core.views import BookingViewSet
from django.urls import include, path
from rest_framework.routers import SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"bookings", BookingViewSet, basename="bookings")


urlpatterns = [path(r"", include((router.urls, "v0"), namespace="v0"))]
