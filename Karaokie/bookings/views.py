from django.shortcuts import render, redirect
from django import views
from bookings.forms import RegisterModelForm

# Create your views here.
class RegisterView(views.View):
    def get(self, request):
        form = RegisterModelForm()
        return render(request, 'Auth/RegisterPage.html', {'registerform': form})
    
    def post(self, request):
        form = RegisterModelForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, 'Auth/RegisterPage.html', {'registerform': form})
    
def Login(request):
    if request.method == "GET":
        return render(request, 'Auth/Login.html')