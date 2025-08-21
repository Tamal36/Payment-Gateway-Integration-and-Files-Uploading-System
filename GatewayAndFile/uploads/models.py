from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from payments.models import UserProfile

class FileUpload(models.Model):
    STATUS_CHOICES      = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user_profile        = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='uploads')
    file                = models.FileField(upload_to='uploadsFiles/')
    filename            = models.CharField(max_length=255)
    upload_time         = models.DateTimeField(auto_now_add=True)
    status              = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    word_count          = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.filename} ({self.get_status_display()})"


class ActivityLog(models.Model):
    user_profile       = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='activity_logs')
    action             = models.CharField(max_length=255)
    metadata           = models.JSONField()
    timestamp          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.action} at {self.timestamp}"