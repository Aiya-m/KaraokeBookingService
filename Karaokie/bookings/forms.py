from django import forms
from bookings.models import Rooms, Booking, Services, BookingServices, Payments
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

class ManageRoomForm(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ["name", "status", "price_per_hour", "capacity", "description","room_image"]
        widgets = {
            "name" : forms.TextInput(attrs={"placeholder": "ชื่อห้อง", "class": "form-control"}),
            "status" : forms.Select(attrs={"class": "form-select"}),
            "price_per_hour" : forms.NumberInput(attrs={"class": "form-control"}),
            "capacity" : forms.NumberInput(attrs={"class": "form-control"}),
            "description" : forms.Textarea(attrs={"placeholder": "คำอธิบาย", "class": "form-control", 'rows': 3}),
            "room_image" : forms.FileInput(attrs={"class": "form-control"})
        }