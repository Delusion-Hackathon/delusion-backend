from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin


from rest_framework.routers import DefaultRouter


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


from .users.views import UserViewSet, UserCreateViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)


urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("admin/", admin.site.urls),
    path(
        "api/v1/users/",
        include([path("", include("delusion.users.urls", namespace="user"))]),
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
