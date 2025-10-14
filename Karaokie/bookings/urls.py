from django.urls import path
from bookings.views import RegisterView, LoginView, CustomerHome, BookingList, CustomerBooking, LogoutView, ManageRoom, EditRoom, CheckInNOut, CustomerHistory

urlpatterns = [
    path('', CustomerHome.as_view(), name='customer-home'),
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
    path("booking/", CustomerBooking.as_view(), name='customer-booking'),
    path("booking/history", CustomerHistory.as_view(), name='customer-history'),
    path('booking/history/cancel/<int:id>/', CustomerHistory.as_view(), name='cancel-booking'),
    path("manager/bookinglist/", BookingList.as_view(), name='bookinglist'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("manager/manageroom/", ManageRoom.as_view(), name='manage-room'),
    path("manager/manageroom/<int:room_id>/", EditRoom.as_view(), name='edit-room-detail'),
    path("manager/CheckIn-Out/", CheckInNOut.as_view(), name='checkinout')
]
