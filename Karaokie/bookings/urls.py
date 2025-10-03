from django.urls import path

from bookings.views import Register
from . import views

urlpatterns = [
    path("", Register.as_view(), name='register'),
    path("login/", views.Login, name='login')
]
