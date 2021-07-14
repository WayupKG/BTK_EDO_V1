from django.contrib import admin
from .models import *


@admin.register(CheckList)
class AdminCheckList(admin.ModelAdmin):
    list_display = ('number', 'author', 'status', 'created', 'updated')
