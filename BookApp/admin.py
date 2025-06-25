from django.contrib import admin
from .models import Room, Booking, TypeRoom

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'room', 'start_date', 'end_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'room')
    search_fields = ('user_name', 'user_email')
    ordering = ('-start_date',)
    list_editable = ('is_confirmed',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'capacity', 'price')  # title заменил на name, если у тебя поле так называется
    list_filter = ('type',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(TypeRoom)
class TypeRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
