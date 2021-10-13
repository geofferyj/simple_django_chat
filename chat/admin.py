from django.contrib import admin
from .models import Chat, Room

# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'receiver', 'message', 'is_read')
    list_filter = ('room', 'sender', 'receiver', 'message', 'is_read')
    search_fields = ('room', 'sender', 'receiver', 'message', 'is_read')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)