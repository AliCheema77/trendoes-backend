from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = UserAdmin.list_display + ('phone_number', 'address')
    fieldsets = UserAdmin.fieldsets + (('Extra Info', {'fields': ('phone_number', 'address')}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Extra Info', {'fields': ('phone_number', 'address')}),)

admin.site.register(User, CustomUserAdmin)
