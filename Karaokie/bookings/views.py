from django.shortcuts import render, redirect
from bookings.models import *
from django.views import View
from bookings.forms import RegisterModelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
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
            messages.success(request, 'Account created successfully.')
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
        return render(request, 'Customer/index.html')
    
class BookingList(View):
    def get(self, request):
        bookinglist = Booking.objects.all()
        return render(request, 'Manager/BookingList.html', context={"booking_list": bookinglist})
