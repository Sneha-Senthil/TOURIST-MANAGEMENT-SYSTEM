# imports 
from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.Main, name="Main"),
    path('Home/', views.Home, name="Home"),
    path('MyBookings/', views.MyBookings, name="MyBookings"),
    path('Login/', views.Login, name="Login"),
    path('Help/', views.Help, name="Help")
]

