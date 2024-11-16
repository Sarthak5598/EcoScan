from django.contrib import admin
from .models import UploadedImage, UserActivity

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'image', 'uploaded_at')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_carbon_emission', 'uploads_count', 'last_activity')
