from django import forms
from bookings.models import Room_type, Rooms, Booking, Services, BookingServices, Payments
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterModelForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]
    
class LoginForm(forms.ModelForm):
    class Meta:
        model =  User
        fields = ["username","password"]
        widgets = {
            "username" : forms.TextInput(attrs={"placeholder": "ชื่อผู้ใช้", "class": "form-control"}),
            "password" : forms.PasswordInput(attrs={"placeholder": "รหัสผ่าน", "class": "form-control"})
        }