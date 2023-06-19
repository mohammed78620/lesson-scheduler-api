from core.views import BookingViewSet, CreateBookingView, UserCreateView
from django.urls import include, path
from rest_framework.routers import SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"", CreateBookingView, basename="")

user_router = OptionalSlashRouter()
user_router.register(r"user_create", UserCreateView, basename="user_create")


core_urlpatterns = [
    path(r"", include((router.urls, "v0"), namespace="v0")),
]
user_urlpatterns = [
    path(r"", include((user_router.urls, "v0"), namespace="v0")),
]
