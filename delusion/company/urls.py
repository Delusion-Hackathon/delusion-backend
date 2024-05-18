from django.urls import path
from . import views


urlpatterns = [
    path('', views.ListCompanyAPIView.as_view()),
    path('add/', views.CreateCompanyAPIView.as_view()),
    path('<int:pk>/', views.DetailCompanyAPIView.as_view()),
    path("tickets/", views.TicketListCreateAPIView.as_view()),
    path("tickets/<int:pk>/", views.TicketDetailAPIView.as_view()),
    path("tickets/<int:pk>/messages/", views.MessageListCreateAPIView.as_view()),
]
