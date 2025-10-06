from django.urls import path

from bookings.views import RegisterView
from . import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", views.Login, name='login')
]
