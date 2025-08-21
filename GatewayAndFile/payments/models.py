from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone           = models.CharField(max_length=15, blank=True)
    address         = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Id{self.id}: {self.user.username}"

class PaymentTransaction(models.Model):
    STATUS_INITIATED    = 0
    STATUS_SUCCESS      = 2
    STATUS_FAILED       = 7

    STATUS_CHOICES      = [
        (STATUS_INITIATED, 'Initiated'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]

    user_profile    = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions')  # ✅ ADD THIS
    transaction_id  = models.CharField(max_length=32, unique=True)
    amount          = models.DecimalField(max_digits=10, decimal_places=2)
    status          = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_INITIATED)
    gateway_response = models.JSONField()
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_profile} - {self.transaction_id} - {self.get_status_display()}"