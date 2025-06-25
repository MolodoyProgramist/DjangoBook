from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_name', 'user_email', 'room', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if room and start_date and end_date:
            overlapping = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            if overlapping:
                raise ValidationError("Вибраний період недоступний для цієї кімнати.")

        return cleaned_data

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    birth_date = forms.DateField(label='Дата народження', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError('Паролі не співпадають')
        return cd.get('password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Ім’я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)