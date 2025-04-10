from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "is_library_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_library_staff",)}),
    )

admin.site.register(User, CustomUserAdmin)
