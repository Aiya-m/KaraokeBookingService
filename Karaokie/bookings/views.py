from django.shortcuts import render, redirect
from django import views

# Create your views here.
class Register(views.View):
    def get(self, request):
        return render(request, './Auth/RegisterPage.html')