from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
import json
import random
import string
from .models import UserActivity,UploadedImage,Tokens,Voucher,UserVoucher
import datetime
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncDate

from .forms import CreateUserForm,UserActive
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
def home(request):
    return render(request, 'caremi/newhome.html')
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            if user.role == 'client':
                return redirect('donate')  # Redirect to the original page after login
            elif user.role == 'employee':
                return redirect('employee')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  # Keep user on login page after failed login attempt

    return render(request, 'caremi/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_image(request):
    if request.user.role == 'client':
        if request.method == 'POST':
            if 'image' not in request.FILES:
                messages.error(request, 'No image file provided')
                return render(request, 'caremi/donate.html')

            try:
                usage, created = UserActivity.objects.get_or_create(user=request.user)
                if usage.last_activity.date() < timezone.now().date():
                    usage.daily_uploads_count = 0
                    usage.last_activity = timezone.now()
               
                if usage.daily_uploads_count >= 20:
                    messages.error(request, 'Daily upload limit reached')
                    return render(request, 'caremi/donate.html', {
                    'daily_uploads_count': usage.daily_uploads_count,
                    'total_carbon_emission': usage.total_carbon_emission,
                    'carbon_emission_response': emission_value,  # Handle error in OpenAI response
                    })
                
                else:
                    image = UploadedImage.objects.create(
                        user=request.user,
                        image=request.FILES['image'],
                        title=request.POST.get('title', ''),
                        status='pending'
                    )
                    load_dotenv()
                    openai.api_key = OPENAI_API_KEY
                    image_path = f"D:\EcoScan\media\{image.image}"
                    with open(image_path, "rb") as image_file:
                        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
                    client = OpenAI(api_key=OPENAI_API_KEY)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                            "role": "user",
                            "content": [
                                {
                                "type": "text",
                                "text": "Detect the clothes and give me the sum of estimated carbon emmision for making them in kg. Just give the number without any units",
                                },
                                {
                                "type": "image_url",
                                "image_url": {
                                    "url":  f"data:image/jpeg;base64,{base64_image}"
                                },
                                },  
                            ],
                            }
                        ],
                        max_tokens=2,
                    )
                    usage.daily_uploads_count = usage.daily_uploads_count + 1
                    emission_value = response.choices[0].message.content.strip()
                    emission_value = emission_value.rstrip(".")
                    image.emission=emission_value
                    image.save()
                    usage.save()

                    messages.success(request, 'Image uploaded and processed successfully!')
                    return render(request, 'caremi/donate.html', {
                        'daily_uploads_count': usage.daily_uploads_count,
                        'carbon_emission_response': emission_value,
                        'image':image
                    })

            except Exception as e:
                messages.error(request, f'Error processing image: {str(e)}')
                return render(request, 'caremi/donate.html', {
                    'daily_uploads_count': usage.daily_uploads_count,
                    'total_carbon_emission': usage.total_carbon_emission,
                    'carbon_emission_response': 'Error processing response',
                })
        else:
            return render(request, 'caremi/donate.html')
    else:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

@login_required(login_url='login')
def client_side(request):
    if request.user.role == 'employee':
        if request.method == 'GET':
            pending_images = UploadedImage.objects.filter(status='pending')
            return render(request, 'caremi/employee_dashboard.html', {
                'pending_images': pending_images,
            })
        
        elif request.method == 'POST':
            try:
                action = request.POST.get('action')
                image_id = request.POST.get('image_id')

                model = UploadedImage.objects.filter(id=image_id).first()
                if not model:
                    return JsonResponse({'error': 'Image not found'}, status=404)

                token = Tokens.objects.filter(user=model.user).first()
                user_activity = UserActivity.objects.filter(user=model.user).first()

                if not token or not user_activity:
                    return JsonResponse({'error': 'Token or User Activity not found'}, status=404)

                if action == 'approve':
                    model.status = 'approved'
                    model.save()
                    if user_activity.total_carbon_emission >= 5:
                        tokens_to_add = user_activity.total_carbon_emission // 5
                        token.token += tokens_to_add
                        user_activity.total_carbon_emission -= tokens_to_add * 5
                        user_activity.save()
                        token.save()
                    success_message = f'Image {image_id} approved.'
                elif action == 'reject':
                    model.status = 'rejected'
                    model.save()
                    success_message = f'Image {image_id} rejected.'
                else:
                    return JsonResponse({'error': 'Invalid action'}, status=400)

                pending_images = UploadedImage.objects.filter(status='pending')
                return render(request, 'caremi/employee_dashboard.html', {
                    'pending_images': pending_images,
                    'success': success_message,
                })

            except Exception as e:
                return JsonResponse({'error': f'Error processing employee action: {str(e)}'}, status=400)

        
    else:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)

@login_required(login_url='login')
def user_dashboard(request):
    if request.user.role == 'client':
        uploaded_images = UploadedImage.objects.filter(user=request.user)
        pending_images = uploaded_images.filter(status='pending')
        accepted_images = uploaded_images.filter(status='approved')
        rejected_images = uploaded_images.filter(status='rejected')
        emissions_data = (
        UploadedImage.objects.filter(user=request.user)
        .annotate(date=TruncDate('uploaded_at'))  # Group by date
        .values('date')
        .annotate(total_emission=Sum('emission'))  # Calculate total emission for each date
        .order_by('date')
        )
        user_activity, _ = UserActivity.objects.get_or_create(user=request.user)
        user_tokens, _ = Tokens.objects.get_or_create(user=request.user, defaults={'token': 0})
        context = {
            'emissions_data': list(emissions_data),
            'username': request.user.username,
            'tokens': user_tokens.token,
            'total_images': uploaded_images.count(),
            'total_emission': user_activity.total_carbon_emission,
            'last_upload': uploaded_images.latest('uploaded_at').uploaded_at if uploaded_images.exists() else None,
            'pending_images': pending_images,
            'accepted_images': accepted_images,
            'rejected_images': rejected_images,
        }

        return render(request, 'caremi/user_dashboard.html', context)
    else:
        return JsonResponse({'error': 'Unauthorized access'}, status=403)


@login_required
def voucher_list(request):
    if request.method == 'GET':
        vouchers = Voucher.objects.filter(is_active=True)
        user_tokens = Tokens.objects.get(user=request.user)
        context = {
            "vouchers": vouchers,
            "user_tokens": user_tokens.token,
        }
        return render(request, "caremi/voucher_list.html", context)
    
    try:
        data = json.loads(request.body)
        voucher_id = data.get('voucher_id')
        
        if not voucher_id:
            return JsonResponse({"error": "Voucher ID is required"}, status=400)

        voucher = get_object_or_404(Voucher, id=voucher_id, is_active=True)
        user_tokens = Tokens.objects.get(user=request.user)

        # Check if user already has this voucher
        if UserVoucher.objects.filter(user=request.user, voucher=voucher).exists():
            return JsonResponse({
                "error": "You have already redeemed this voucher"
            }, status=400)

        # Check if user has enough tokens
        if user_tokens.token < voucher.token_cost:
            return JsonResponse({
                "error": "You do not have enough tokens to redeem this voucher"
            }, status=400)

        user_tokens.token -= voucher.token_cost
        user_tokens.save()

        UserVoucher.objects.create(user=request.user, voucher=voucher)

        return JsonResponse({
            "success": f"Successfully redeemed {voucher.name}",
            "voucher_code": voucher.code,
            "new_token_balance": user_tokens.token
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid request format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

