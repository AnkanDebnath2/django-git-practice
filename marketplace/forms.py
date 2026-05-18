from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FlatListing, Message, Booking, UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'location', 'bio']


class FlatListingForm(forms.ModelForm):
    class Meta:
        model = FlatListing
        fields = ['title', 'description', 'location', 'price', 'size', 'bedrooms', 'bathrooms', 'image_url', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4}),
        }


class BookingRequestForm(forms.ModelForm):
    visit_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Booking
        fields = ['visit_date', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }
