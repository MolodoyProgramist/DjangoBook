from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone





class BookingManager(models.Manager):
    def is_room_available(self, room, start_date, end_date):
        # Проверяет, есть ли пересечения с уже существующими бронями
        return not self.filter(
            room=room,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).exists()

    def confirmed(self):
        # Вернуть только подтверждённые брони (если есть поле status)
        return self.filter(status='confirmed')

    def active(self):
        # Брони, которые сейчас активны (например, end_date позже текущей даты)
        now = timezone.now().date()
        return self.filter(end_date__gte=now)



class TypeRoom(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Room(models.Model):
    objects = BookingManager()
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TypeRoom, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rooms_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)


    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('confirmed', 'Підтверджено'),
        ('canceled', 'Відмінено'),
    ]

    objects = BookingManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user_name} - {self.room.name}"

class Profile(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Create your models here.
