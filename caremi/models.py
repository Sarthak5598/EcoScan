from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_images")
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="activity")
    total_carbon_emission = models.FloatField(default=0.0)
    daily_uploads_count = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(default=timezone.now().date())

    def __str__(self):
        return f"Activity for {self.user.username}"
