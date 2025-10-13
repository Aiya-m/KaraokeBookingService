from django.urls import path
from bookings.views import RegisterView, LoginView, CustomerHome, BookingList, CustomerBooking, LogoutView, ManageRoom

urlpatterns = [
    path('', CustomerHome.as_view(), name='customer-home'),
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("booking/", CustomerBooking.as_view(), name='customer-booking'),
    path("manager/bookinglist/", BookingList.as_view(), name='bookinglist'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("manager/manageroom/", ManageRoom.as_view(), name='manage-room')
]
