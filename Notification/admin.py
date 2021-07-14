from django.contrib import admin
from .models import *


@admin.register(Notification)
class AdminNotification(admin.ModelAdmin):
    list_display = ('user', 'body', 'view', 'created', 'updated')

