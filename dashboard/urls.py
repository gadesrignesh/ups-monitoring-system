from django.urls import path
from . import views

urlpatterns = [
    path('', views.splash),
    path('home', views.home),
    path('ups1', views.ups1),
]
