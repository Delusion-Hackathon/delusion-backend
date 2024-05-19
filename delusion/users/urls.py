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

    path("me/", views.UserMeViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name="user-me"),

    path("nodes/", views.NodeListCreateView.as_view(), name="node-list-create"),
    path("nodes/<int:pk>/", views.NodeRetrieveUpdateDestroyView.as_view(), name="node-retrieve-update-destroy"),
    path("nodes/node_id/<str:node_id>/", views.NodeRetrieveWithNodeIDView.as_view(), name="node-retrieve-with-node-id"),
]
