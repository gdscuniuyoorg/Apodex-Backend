from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model



user = get_user_model()
class CustomUserAdmin(UserAdmin):
    model = user
    list_display = ['email', 'is_active', 'is_staff']
    
    ordering = ['email']

admin.site.register(user, CustomUserAdmin)
