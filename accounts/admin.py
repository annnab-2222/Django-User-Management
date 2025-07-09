from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'birth_date']
    list_filter = ['location', 'birth_date']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['user']


# Register your models here.
# Register User model if needed (usually already registered)
# Register Profile model if you have one
