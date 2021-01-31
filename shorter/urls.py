from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<short_url>/', views.redirect_to_url),
    path('info/<short_url>/', views.info_about_url),
]
