from django.urls import path
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView,
                                            TokenObtainPairView)
from . import views



app_name = "user"


urlpatterns = [
    # JWTToken
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', views.UserCreateViewSet.as_view({'post': 'create'}), name="user-create"),

    path('company-register/', views.CompanyRegistrationViewSet.as_view({'post': 'create'}), name="company-register"),
    path('countries/', views.CountryViewSet.as_view({'get': 'list'}), name="countries"),
    path("me/", views.UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name="user-me"),
]
