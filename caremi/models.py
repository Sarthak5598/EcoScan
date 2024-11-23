from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    groups = models.ManyToManyField(
        Group,
        related_name="caremi_user_groups",  # Unique related name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="caremi_user_permissions",  # Unique related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class UploadedImage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_images")
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    emission = models.FloatField(default=0.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return self.title or f"Image {self.id}"

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="activity")
    total_carbon_emission = models.FloatField(default=0.0)
    daily_uploads_count = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Activity for {self.user.username} {self.total_carbon_emission}"

class Tokens(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.IntegerField(default=0)

class Voucher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    code = models.CharField(default="GOGREEN",max_length=10)
    token_cost = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)  # Only active vouchers are redeemable
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserVoucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="redeemed_vouchers")
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} redeemed {self.voucher.name}"
