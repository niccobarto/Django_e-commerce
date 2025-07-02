# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserAddress

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone','image_profile'),}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('phone','image_profile'),}),
    )

    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
    ]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserAddress)
