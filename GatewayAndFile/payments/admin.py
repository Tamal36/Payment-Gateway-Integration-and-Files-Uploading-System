from django.contrib import admin
from .models import *
# Register your models here.

class UserProfileInline(admin.StackedInline):
    model               = UserProfile
    can_delete          = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(admin.ModelAdmin):
    inlines             = (UserProfileInline,)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display        = ['id', 'user', 'phone', 'address', 'created_at']
    search_fields       = ['user__username', 'phone']

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display        = ['transaction_id', 'get_username', 'amount', 'status', 'timestamp']
    search_fields       = ['transaction_id', 'user_profile__user__username']
    list_filter         = ['status', 'timestamp']

    @admin.display(description="Username")
    def get_username(self, obj):
        return obj.user_profile.user.username
