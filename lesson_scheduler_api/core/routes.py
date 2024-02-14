from core.views import BookingViewSet, CreateBookingView, SignInAPI, SignUpAPI, UpdateUserDetails
from django.urls import include, path
from knox import views as knox_views
from rest_framework.routers import SimpleRouter


class OptionalSlashRouter(SimpleRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


router = OptionalSlashRouter()
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"", CreateBookingView, basename="")

user_router = OptionalSlashRouter()
user_router.register(r"user", SignInAPI, basename="user")
user_router.register(r"user", SignUpAPI, basename="user")
user_router.register(r"user", UpdateUserDetails, basename="user")


core_urlpatterns = [
    path(r"", include((router.urls, "v0"), namespace="v0")),
]
user_urlpatterns = [
    path(r"", include((user_router.urls, "v0"), namespace="v0")),
    path("api/auth/logout", knox_views.LogoutView.as_view(), name="knox-logout"),
]
