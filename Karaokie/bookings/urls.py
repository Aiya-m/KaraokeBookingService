from django.urls import path
from bookings.views import RegisterView, LoginView, CustomerHome
from . import views

urlpatterns = [
    path('/', CustomerHome.as_view(), name='customer-home'),
    path("/register/", RegisterView.as_view(), name='register'),
    path("/login/", LoginView.as_view(), name='login')
]
