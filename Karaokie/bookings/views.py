from django.shortcuts import render, redirect
from bookings.models import *
from django.views import View
from bookings.forms import RegisterModelForm, LoginForm
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
        form = LoginForm()
        return render(request, 'login', {"loginform": form})

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
        bookinglist = Booking.objects.all()
        return render(request, 'Manager/BookingList.html', context={"booking_list": bookinglist})
