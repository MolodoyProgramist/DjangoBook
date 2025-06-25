from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BookingForm, UserRegistrationForm, UserLoginForm
from django.contrib import messages

from .models import Booking, Room, Profile


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user  # Привязываем текущего пользователя
                booking.user_name = request.user.get_full_name() or request.user.username
                booking.user_email = request.user.email
            booking.save()
            return redirect('success_page')  # или куда у тебя после создания брони
    else:
        form = BookingForm()
    return render(request, 'BookApp/booking_form.html', {'form': form})



def my_bookings(request):
    email = request.GET.get('email')
    bookings = Booking.objects.none()
    if email:
        bookings = Booking.objects.filter(user_email=email)
    return render(request, 'BookApp/my_bookings.html', {'bookings': bookings})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            # создаём профиль с датой рождения
            Profile.objects.create(user=new_user, birth_date=form.cleaned_data['birth_date'])
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # главная страница после входа
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    return render(request, 'home.html')

@login_required
def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms_list.html', {'rooms': rooms})

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('home')  # или куда хочеш перенаправити