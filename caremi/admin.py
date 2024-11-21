from django.contrib import admin
from .models import UploadedImage, UserActivity,User,Tokens,Voucher,UserVoucher

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

@admin.register(Tokens)
class TokensAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'token_cost', 'is_active', 'created_at')

@admin.register(UserVoucher)
class UserVoucherAdmin(admin.ModelAdmin):
    list_display = ('user', 'voucher', 'redeemed_at')