from django.urls import path

from bookings.views import RegisterView, CustomerHome
from . import views

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", views.Login, name='login'),
    path("customer/home/", CustomerHome.as_view(), name='customer-home')
]
