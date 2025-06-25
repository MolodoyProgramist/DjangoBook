from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import create_booking
#login
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home_view, name='home'),


    # твои уже существующие
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/', views.create_booking, name='create_booking'),
    path('rooms/', views.rooms_list, name='rooms_list'),

]
