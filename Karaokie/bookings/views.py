from django.shortcuts import render, redirect
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
            login(request, user)
            return redirect(request, '')
        else:
            return render(request, 'Auth/Login.html', {"form": None})
        
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'Auth/Login.html', {"form": None})

class CustomerHome(View):
    def get(self, request):
        return render(request, 'Customer/index.html')
