from django.urls import path

from bookings.views import Register

urlpatterns = [
    path("", Register.as_view(), name='register'),
]
