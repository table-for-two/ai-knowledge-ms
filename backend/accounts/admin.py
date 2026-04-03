from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active',
                    'last_login_at', 'created_at', 'updated_at')
    list_filter = ('is_staff', 'is_active')
    
    ordering = ('email',)
