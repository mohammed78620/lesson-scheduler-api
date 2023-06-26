from core.routes import core_urlpatterns, user_urlpatterns
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from core.routes import user_urlpatterns


urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(api_version="v0"), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += [
    path("core/", include(core_urlpatterns)),
    path("", include(user_urlpatterns)),
]
