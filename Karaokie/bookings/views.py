from django.shortcuts import render, redirect
from django import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from bookings.forms import RegisterModelForm
from django.contrib import messages

# Create your views here.
class RegisterView(views.View):
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

class CustomerHome(views.View):
    def get(self, request):
        return render(request, 'Customer/index.html')

def Login(request):
    if request.method == "GET":
        return render(request, 'Auth/Login.html')