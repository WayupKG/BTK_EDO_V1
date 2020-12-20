from django.contrib import admin
from .models import *


@admin.register(Document)
class AdminDocument(admin.ModelAdmin):
    list_display = ('number', 'author', 'name', 'created', 'updated')


@admin.register(FileDocument)
class AdminFileDocument(admin.ModelAdmin):
    list_display = ('document', 'created')


@admin.register(MovementOfDocument)
class AdminMovementOfDocument(admin.ModelAdmin):
    list_display = ('responsible', 'document', 'status', 'created', 'updated')


@admin.register(ReplyDocument)
class AdminReplyDocument(admin.ModelAdmin):
    list_display = ('movement', 'appointment', 'status', 'created', 'updated')


@admin.register(FileReplyDocument)
class AdminFileReplyDocument(admin.ModelAdmin):
    list_display = ('reply', 'created')
