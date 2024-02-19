from django.contrib import admin

from django.contrib import admin
from .models import ColorUser  # Assuming that ColorUser is in the same directory as admin.py

@admin.register(ColorUser)
class ColorUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'color', 'date')
    search_fields = ('user__username',)

