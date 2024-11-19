from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserActivity,UploadedImage

class CreateUserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('employee', 'Employee'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class UserActive(forms.ModelForm):
    class Meta:
        model = UserActivity
        fields = ['user','total_carbon_emission' ,'daily_uploads_count','last_activity']
        