from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
import json
import random
import string
from .models import UserActivity,UploadedImage
import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm,UserActive
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            return redirect('home')  # Redirect to the original page after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Keep user on login page after failed login attempt

    return render(request, 'caremi/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_image(request):
    print(f"Request method: {request.method}")

    if request.user.role == 'client':
        if 'image' not in request.FILES:
            print("sadndanmddmasds")
            messages.error(request, 'No image file provided')
            return render(request, 'caremi/home.html')

        try:
            # Get or create user activity
            usage, created = UserActivity.objects.get_or_create(user=request.user)
            
            # Reset count if it's a new day
            if usage.last_activity.date() < timezone.now().date():
                usage.daily_uploads_count = 0
                usage.last_activity = timezone.now()
            print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            # Check daily limit
            if usage.daily_uploads_count >= 4:
                print("asdfghjhgfdsdfghjhgfdsasdfgh")
                messages.error(request, 'Daily upload limit reached')
                return render(request, 'caremi/home.html')
            print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            # Create image record
            image = UploadedImage.objects.create(
                user=request.user,
                image=request.FILES['image'],
                title=request.POST.get('title', ''),
                status='pending'
            )
            print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            # Generate the full URL for the uploaded image
            image_url = f"{request.scheme}://{request.get_host()}/media/{image.image}"
            print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            # Process with OpenAI (assuming OpenAI logic is correct)
            client = OpenAI(api_key=OPENAI_API_KEY)
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
                            "url": image_url,
                        },
                        },
                    ],
                    }
                ],
                max_tokens=2,
            )
            print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            usage.daily_uploads_count += 1
            print("shdajkasddsjashjdsahjdjdjdsajdajdajdjaj"+usage.daily_uploads_count)
            usage.total_carbon_emission += float(response.choices[0].message.content.strip())
            usage.save()

            messages.success(request, 'Image uploaded and processed successfully!')
            return render(request, 'caremi/home.html', {
                'daily_uploads_count': usage.daily_uploads_count,
                'total_carbon_emission': usage.total_carbon_emission,
                'carbon_emission_response': response,  # Handle error in OpenAI response
            })

        except Exception as e:
            messages.error(request, f'Error processing image: {str(e)}')
            return render(request, 'caremi/home.html', {
                'daily_uploads_count': usage.daily_uploads_count,
                'total_carbon_emission': usage.total_carbon_emission,
                'carbon_emission_response': 'Error processing response',  # Handle error in OpenAI response
            })

    # Employee-specific behavior
    elif request.user.role == 'employee':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            image_id = data.get('image_id')

            model = UploadedImage.objects.filter(id=image_id).first()
            if not model:
                pending_images = UploadedImage.objects.filter(status='pending')
                return render(request, 'caremi/employee_dashboard.html', {
                    'pending_images': pending_images,
                    'error': 'Image not found',
                })

            if action == 'approve':
                model.status = 'approved'
                model.save()
                success_message = f'Image {image_id} approved.'
            elif action == 'reject':
                model.status = 'rejected'
                model.save()
                success_message = f'Image {image_id} rejected.'
            else:
                pending_images = UploadedImage.objects.filter(status='pending')
                return render(request, 'caremi/employee_dashboard.html', {
                    'pending_images': pending_images,
                    'error': 'Invalid action',
                })

            pending_images = UploadedImage.objects.filter(status='pending')
            return render(request, 'caremi/employee_dashboard.html', {
                'pending_images': pending_images,
                'success': success_message,
            })

        except Exception as e:
            return JsonResponse({'error': f'Error processing employee action: {str(e)}'}, status=400)

    else:
        # Return Unauthorized if the user role is not recognized
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
