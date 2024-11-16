from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
import json
import random
import string
from .models import URL,UserUsage
import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm,UserActivity
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from openai import OpenAI


def registration_page(request):
    form = CreateUserForm()
    if request.method=='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error in registration')
    return render(request, 'caremi/registration.html', {'form': form})


def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password= request.POST.get('password')

        user= authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You have been successfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'caremi/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_image(request):
    if request.method=='POST':
        data = json.loads(request.body)
        image = data.get('image')
        usage, created = UserUsage.objects.get_or_create(user=request.user)
        
        # Reset count if it's a new day
        if usage.last_activity < timezone.now().date():
            usage.daily_uploads_count = 0
            usage.last_activity = timezone.now().date()
        
        if usage.daily_uploads_count >= 4:
            messages.error(request, 'error: Daily limit reached')
            return JsonResponse({'error': 'Daily limit reached'}, status=400)
        else:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Estimate the total carbon emissions in kg CO₂ for the detected clothing in the image."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": "http://127.0.0.1:8000/media/uploaded_images/{image}",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=2,
            )
            usage.daily_uploads_count += 1
            usage.total_carbon_emission += response
            usage.save()
        
    return render(request, 'caremi/home.html' , {'response': response})