from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView


from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions


from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .users.views import UserViewSet, UserCreateViewSet



router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('admin/', admin.site.urls),
    path('api/v1/users/', include([path("", include("delusion.users.urls", namespace="user"))])),
    path('api/v1/companies/', include('delusion.company.urls')),
    path('api/v1/nodes/', include('delusion.node.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
