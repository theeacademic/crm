from django.contrib import admin
from .models import Client
from django.contrib.auth.admin import UserAdmin


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'field', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'field')
    list_filter = ('field',)
