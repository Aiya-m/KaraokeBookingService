from django.shortcuts import render, redirect
from bookings.models import *
from django.views import View
from bookings.forms import RegisterModelForm, LoginForm, ManageRoomForm
from bookings.models import Rooms
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'Auth/RegisterPage.html', {'registerform': form})

    def post(self, request):
        form = RegisterModelForm(request.POST)

        if form.is_valid():
            print('valid form')
            user = form.save()
            group = Group.objects.get(name="Customer")
            user.groups.add(group)
            messages.success(request, 'สร้างบัญชีสำเร็จ')
            login(request, user)
            return redirect('customer-home')
        else:
            print('invalid form:', form.errors)
        return render(request, 'Auth/RegisterPage.html', {'registerform': form})
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'Auth/Login.html', {'loginform': form})
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff :
                return redirect('bookinglist')
            else:
                return redirect('customer-home')
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
            form = LoginForm(request.POST)
            return render(request, 'Auth/Login.html', {"loginform": form})
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class CustomerHome(View):
    def get(self, request):
        bigRooms = Rooms.objects.filter(room_type__name='ห้องขนาดใหญ่')
        mediumRooms = Rooms.objects.filter(room_type__name='ห้องขนาดกลาง')
        smallRooms = Rooms.objects.filter(room_type__name='ห้องขนาดเล็ก')
        return render(request, 'Customer/index.html', {
            'bigRooms': bigRooms,
            'mediumRooms': mediumRooms,
            'smallRooms': smallRooms
            })

class CustomerBooking(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'Customer/bookingPage.html')
        else:
            return redirect('login')

    
class BookingList(View):
    def get(self, request):
        booking_pending = Booking.objects.filter(booking_status=Booking.Booking_status.Pending)
        return render(request, 'Manager/BookingList.html', context={"booking_pending": booking_pending})
    def post(self, request):
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        if not booking_id:
            return redirect("bookinglist")

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return redirect("bookinglist")
        if action == "reject":
            booking.delete()

        elif action == "confirm":
            booking.booking_status = Booking.Booking_status.Check_In
            booking.save()

        return redirect("bookinglist")
    
class ManageRoom(View):
    def get(self, request):
        form = ManageRoomForm()
        bigRoom = Rooms.objects.filter(room_type=Rooms.Type.Large)
        medRoom = Rooms.objects.filter(room_type=Rooms.Type.Medium)
        smlRoom = Rooms.objects.filter(room_type=Rooms.Type.Small)
        return render(request, 'Manager/ManageRoom.html', context={"bigroom": bigRoom, "medroom": medRoom, "smlRoom": smlRoom, "manageroomform": form})
    
class EditRoom(View):
    def get(self, request, room_id):
        room = Rooms.objects.get(pk=room_id)
        form = ManageRoomForm(instance=room)
        return render(request, 'Manager/ManageRoomDetail.html', context={"room": room, "manageroomform": form})
    
    def post(self, request, room_id):
        room = Rooms.objects.get(pk=room_id)
        form = ManageRoomForm(request.POST, request.FILES, instance=room)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('manage-room')
        else:
            print(form.errors)
        return redirect('manage-room')
    
class CheckInNOut(View):
    def get(self, request):
        booking_checkin = Booking.objects.filter(booking_status=Booking.Booking_status.Check_In)
        booking_checkout = Booking.objects.filter(booking_status=Booking.Booking_status.Check_Out)
        return render(request, 'Manager/CheckInNOut.html', context={"booking_checkin": booking_checkin, "booking_checkout": booking_checkout})
    
    def post(self, request):
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return redirect("checkinout")

        if action == "checkout":
            booking.booking_status = Booking.Booking_status.Check_Out
            booking.room.status = Rooms.Status.Empty
            booking.room.save()
            booking.save()

        return redirect("checkinout")
