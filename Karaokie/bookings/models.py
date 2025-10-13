from django.db import models
from datetime import datetime, timedelta

class Rooms(models.Model):
    class Status(models.TextChoices):
        Reserved = "จองแล้ว"
        InUse = "กำลังใช้งาน"
        Empty = "ห้องว่าง"

    class Type(models.TextChoices):
        Large = "ห้องขนาดใหญ่"
        Medium = "ห้องขนาดกลาง"
        Small = "ห้องขนาดเล็ก"

    name = models.CharField(max_length=50, unique=True, null=False)
    status = models.CharField(max_length=20, choices=Status.choices)
    price_per_hour = models.IntegerField(null=False, default=0)
    room_type = models.CharField(max_length=20, choices=Type.choices)
    capacity = models.IntegerField(null=False, default=0)
    description = models.CharField(max_length=200, null=True)


class Services(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    price = models.IntegerField(null=False)

class Booking(models.Model):
    class Booking_status(models.TextChoices):
        Pending = "รอดำเนินการ"
        Confirmed = "ยืนยันการจอง"
        Rejected = "ปฏิเสธ"
        Cancel = "ยกเลิก"
        Check_In = "เช็กอิน"
        Check_Out = "เช็กเอาท์"

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='booking')
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    number_of_customer = models.IntegerField(null=False)
    booking_date = models.DateField(null=False)
    start_time = models.TimeField(null=False)
    end_time = models.TimeField(null=False)
    phone = models.CharField(max_length=20, null=False, default="")
    booking_status = models.CharField(max_length=20, choices=Booking_status.choices)
    notes = models.CharField(max_length=200, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    service = models.ManyToManyField(Services)

    def get_book_time(self):
        start = self.start_time.strftime("%H:%M")
        end = self.end_time.strftime("%H:%M")
        return f"{start} - {end}"
    
    def get_price(self, room):
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)

        duration = (end_datetime - start_datetime)/3600
        price = duration.total_seconds() * room.price_per_hour
        return price



class BookingServices(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class Payments(models.Model):
    class Pay_status(models.TextChoices):
        Pending = "รอดำเนินการ"
        Paid = "ชำระเงินแล้ว"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_slip = models.BinaryField(null=False)
    payment_status = models.CharField(max_length=20, choices=Pay_status.choices)
    pay_date = models.DateTimeField(null=False)
