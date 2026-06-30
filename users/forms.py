from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from users.models import UserProfile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    pass


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=15)
    shipping_address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'shipping_address', 'city']