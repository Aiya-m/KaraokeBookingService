from django.shortcuts import render, redirect
from bookings.models import *
from django.views import View
from bookings.forms import RegisterModelForm, LoginForm, ManageRoomForm, BookingForm, ServicesForm, RoomsForm, PaymentsForm, ServiceEditForm, CustomerUpdateForm
from bookings.models import Rooms
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.utils import timezone

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
            if user.groups.filter(name='Manager').exists() :
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
        bigRooms = Rooms.objects.filter(room_type='ห้องขนาดใหญ่')
        mediumRooms = Rooms.objects.filter(room_type='ห้องขนาดกลาง')
        smallRooms = Rooms.objects.filter(room_type='ห้องขนาดเล็ก')
        return render(request, 'Customer/index.html', {
            'bigRooms': bigRooms,
            'mediumRooms': mediumRooms,
            'smallRooms': smallRooms
            })

class CustomerBooking(PermissionRequiredMixin, View):
    permission_required = ["bookings.add_booking", "bookings.delete_booking", "bookings.view_booking", "bookings.view_services", "bookings.view_rooms"]
    def get(self, request):
        bookingform = BookingForm()
        roomsform = RoomsForm()
        servicesform = ServicesForm()
        paymentsform = PaymentsForm()
        return render(request, 'Customer/bookingPage.html', {
            'bookingform': bookingform,
            'roomsform': roomsform,
            'servicesform': servicesform,
            'paymentsform': paymentsform
        })
        
    def post(self, request):
        rooms_form = RoomsForm(request.POST)
        services_form = ServicesForm(request.POST)
        booking = BookingForm(request.POST)
        payment = PaymentsForm(request.POST, request.FILES)

        selected_room = None

        try:
            with transaction.atomic():
                if rooms_form.is_valid() and booking.is_valid() and payment.is_valid():
                    selected_room = rooms_form.cleaned_data.get('room')
                    booking_obj = booking.save(commit=False)
                    booking_obj.user = request.user
                    booking_obj.booking_status = Booking.Booking_status.Pending

                    if not selected_room:
                        booking.add_error(None, "กรุณาเลือกห้องก่อนทำการจอง")
                        raise ValueError("No room selected")

                    booking_obj.room = selected_room

                    booking_date = booking_obj.booking_date
                    start_time = booking_obj.start_time
                    end_time = booking_obj.end_time
                    number_of_customer = booking_obj.number_of_customer

                    if number_of_customer > selected_room.capacity:
                        booking.add_error("number_of_customer", f"จำนวนคนไม่ควรเกิน {selected_room.capacity} คน")

                    if booking_date < timezone.now().date():
                        booking.add_error("booking_date", "ไม่สามารถเลือกวันที่ย้อนหลังได้")

                    if start_time >= end_time:
                        booking.add_error(None, "เวลาใช้บริการไม่ถูกต้อง")

                    overlap = Booking.objects.filter(
                        room=selected_room,
                        booking_date=booking_date,
                        start_time__lt=end_time,
                        end_time__gt=start_time
                    ).exists()
                    if overlap:
                        booking.add_error(None, "ช่วงเวลานี้ถูกจองไปแล้ว")

                    if booking.errors:
                        raise ValueError("Booking validation failed")

                    booking_obj.save()

                    if services_form.is_valid():
                        selected_services = services_form.cleaned_data.get('services')
                        if selected_services:
                            booking_obj.service.set(selected_services)

                    payment_obj = payment.save(commit=False)
                    payment_obj.booking = booking_obj
                    payment_obj.save()

                    print("inserted in db")
                    return redirect("customer-history")

                else:
                    print("Form invalid:", booking.errors, rooms_form.errors, payment.errors)
                    raise transaction.TransactionManagementError("Invalid form input")

            return redirect('customer-history')
        except Exception as e:
            print("transaction exception", e)
            return render(request, "Customer/bookingPage.html", {
                "bookingform": booking,
                "roomsform": rooms_form,
                "servicesform": services_form,
                "paymentsform": payment,
            })
        
class CustomerHistory(PermissionRequiredMixin, View):
    permission_required = ["bookings.delete_booking", "bookings.view_booking", "bookings.view_services", "bookings.view_rooms", "bookings.view_payments"]
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'Customer/historyPage.html', {
            'bookings': bookings
        })
    
    def post(self, request, id):
        booking = Booking.objects.get(id=id)
        booking.delete()

        return redirect('customer-history')

class CustomerProfile(PermissionRequiredMixin, View):
    permission_required = ["auth.change_user", "auth.view_user"]
    def get(self, request):
        user = request.user
        edit_mode = request.GET.get('edit') == '1'
        form = CustomerUpdateForm(instance=user)
        return render(request, 'Customer/profilePage.html', {
            'registerform': form,
            'edit_mode': edit_mode
        })

    def post(self, request):
        user = request.user
        form = CustomerUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('customer-profile')
        return render(request, 'Customer/profilePage.html', {
            'registerform': form,
            'edit_mode': True 
        })
    
class BookingList(PermissionRequiredMixin, View):
    permission_required = ["bookings.delete_booking"]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            booking_pending = Booking.objects.filter(booking_status=Booking.Booking_status.Pending).order_by('create_date')
            return render(request, 'Manager/BookingList.html', context={"booking_pending": booking_pending})
        else:
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")

    def post(self, request):
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = Booking.objects.get(id=booking_id)

        if action == "reject":
            booking.delete()

        elif action == "confirm":
            booking.booking_status = Booking.Booking_status.Check_In
            booking.save()

        return redirect("bookinglist")
    
class ManageRoom(PermissionRequiredMixin, View):
    permission_required = ["bookings.view_rooms", "bookings.change_services"]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            form = ManageRoomForm()
            serviceform = ServiceEditForm()
            bigRoom = Rooms.objects.filter(room_type=Rooms.Type.Large)
            medRoom = Rooms.objects.filter(room_type=Rooms.Type.Medium)
            smlRoom = Rooms.objects.filter(room_type=Rooms.Type.Small)
            service = Services.objects.all()
            return render(request, 'Manager/ManageRoom.html', context={"bigroom": bigRoom, "medroom": medRoom, "smlRoom": smlRoom, "service": service, "manageroomform": form, "serviceedit": serviceform})
        else:
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
    
    def post(self, request):
        if 'edit_service' in request.POST:
            service_id = request.POST.get('service_id')
            service = Services.objects.get(pk=service_id)
            form = ServiceEditForm(request.POST, instance=service)
            if form.is_valid():
                form.save()
                return redirect('manage-room')

class EditRoom(PermissionRequiredMixin, View):
    permission_required = ["bookings.change_rooms"]
    def get(self, request, room_id):
        if request.user.groups.filter(name='Manager').exists():
            room = Rooms.objects.get(pk=room_id)
            form = ManageRoomForm(instance=room)
            return render(request, 'Manager/ManageRoomDetail.html', context={"room": room, "manageroomform": form})
        else:
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
    
    def post(self, request, room_id):
        room = Rooms.objects.get(pk=room_id)
        form = ManageRoomForm(request.POST, request.FILES, instance=room)
        print(form.is_valid())
        try:
            with transaction.atomic():
                if form.is_valid():
                    form.save()
                    return redirect('manage-room')
                else:
                    print(form.errors)
                    return render(request, "Manager/ManageRoomDetail.html", context={"room": room, "manageroomform": form})
            raise transaction.TransactionManagementError("Error")
        except Exception as e:
            raise e
    
class CheckInNOut(PermissionRequiredMixin, View):
    permission_required = ["bookings.change_booking"]
    def get(self, request):
        if request.user.groups.filter(name='Manager').exists():
            booking_checkin = Booking.objects.filter(booking_status=Booking.Booking_status.Check_In).order_by('create_date')
            booking_checkout = Booking.objects.filter(booking_status=Booking.Booking_status.Check_Out).order_by('create_date')
            return render(request, 'Manager/CheckInNOut.html', context={"booking_checkin": booking_checkin, "booking_checkout": booking_checkout})
        else:
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")
        
    
    def post(self, request):
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")
        booking = Booking.objects.get(id=booking_id)

        if action == "checkin":
            booking.booking_status = Booking.Booking_status.Check_Out
            booking.room.status = Rooms.Status.InUse
            booking.room.save()
            booking.save()
        elif action == "checkout":
            booking.booking_status = Booking.Booking_status.Confirmed
            booking.room.status = Rooms.Status.Empty
            booking.room.save()
            booking.save()

        return redirect("checkinout")

class HistoryView(PermissionRequiredMixin, View):
    permission_required = ["bookings.view_booking"]
    def get(self,request):
        if request.user.groups.filter(name='Manager').exists():
            booking_completed = Booking.objects.filter(booking_status=Booking.Booking_status.Confirmed).order_by('create_date')
            return render(request, 'Manager/BookingHistory.html', context={"booking_completed": booking_completed})
        else:
            return HttpResponseForbidden("คุณไม่มีสิทธิ์เข้าถึงหน้านี้")