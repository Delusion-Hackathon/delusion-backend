from django.urls import path
from . import views


urlpatterns = [
    path('download/linux-bsd/company/<str:company_name>/', views.GetCommandAPIView.as_view()),
    path('download/<int:option>/company/<str:company_name>/', views.DownloadAgentAPIView.as_view()),
    path('create-node/', views.CreateNodeAPIView.as_view()),
]
