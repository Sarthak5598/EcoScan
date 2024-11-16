from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserActivity,UploadedImage

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username' ,'email' , 'password1' , 'password2']

class UserActivity(forms.ModelForm):
    class Meta:
        model = UserActivity
        fields = ['user','total_carbon_emission' ,'uploads_count','last_activity']
        