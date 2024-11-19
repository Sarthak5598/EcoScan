from django.contrib import admin
from .models import UploadedImage, UserActivity,User

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'image', 'uploaded_at')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_carbon_emission', 'daily_uploads_count', 'last_activity')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
