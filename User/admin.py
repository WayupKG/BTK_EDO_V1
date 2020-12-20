from django.contrib import admin
from .models import *


@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    list_display = ('name', 'created')


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'is_active', 'created')


@admin.register(SettingsProfile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('profile', 'is_mail_inbox', 'is_mail_movement', 'is_mail_ad')