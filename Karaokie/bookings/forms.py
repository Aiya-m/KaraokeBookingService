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
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
class LoginForm(forms.ModelForm):
    class Meta:
        model =  User
        fields = ["username","password"]
        widgets = {
            "username" : forms.TextInput(attrs={"placeholder": "ชื่อผู้ใช้", "class": "form-control"}),
            "password" : forms.PasswordInput(attrs={"placeholder": "รหัสผ่าน", "class": "form-control"})
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "number_of_customer",
            "booking_date",
            "start_time",
            "end_time",
            "phone",
            "notes"
        ]

        widgets = {
                "number_of_customer": forms.NumberInput(attrs={
                    "class": "form-control",
                    "min": 1,
                    "placeholder": "10"
                }),
                "booking_date": forms.DateInput(attrs={
                    "type": "date",
                    "class": "form-control",
                    "placeholder": "เลือกวันที่"
                }),
                "start_time": forms.TimeInput(attrs={
                    "type": "time",
                    "class": "form-control"
                }),
                "end_time": forms.TimeInput(attrs={
                    "type": "time",
                    "class": "form-control"
                }),
                "phone": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "เช่น 0812345678"
                }),
            }
        
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 2,
        "placeholder": "หมายเหตุ (ถ้ามี)"
    }))

class RoomsForm(forms.Form):
    room = forms.ModelChoiceField(
        queryset=Rooms.objects.all(),
        empty_label="เลือกห้อง",
        widget=forms.Select(attrs={"class": "form-control"})
    )

class ServicesForm(forms.Form):
    services = forms.ModelMultipleChoiceField(
        queryset=Services.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-control",
            "size": 5
        })
    )

class PaymentsForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = [
            'payment_slip',
            'pay_date',
        ]
        widgets = {
            "pay_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control",
                "placeholder": "เลือกวันที่และเวลา"
            }),
            "payment_slip": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
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

    def clean(self):
        cleaned_data = super().clean()
        capacity = cleaned_data.get("capacity")
        room = self.instance  

        if room and capacity is not None:
            room_type = room.room_type
            
            if room_type == Rooms.Type.Large and capacity > 20:
                self.add_error("capacity", "ห้องขนาดใหญ่รองรับได้ไม่เกิน 20 คน")
            elif room_type == Rooms.Type.Medium and capacity > 10:
                self.add_error("capacity", "ห้องขนาดกลางรองรับได้ไม่เกิน 10 คน")
            elif room_type == Rooms.Type.Small and capacity > 5:
                self.add_error("capacity", "ห้องขนาดเล็กรองรับได้ไม่เกิน 5 คน")

        return cleaned_data

class ServiceEditForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ["name", "price"]
        widgets = {
            "name" : forms.TextInput(attrs={"placeholder": "ชื่อบริการ", "class": "form-control"}),
            "price" : forms.NumberInput(attrs={"placeholder": "ราคา", "class": "form-control"})
        }

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data