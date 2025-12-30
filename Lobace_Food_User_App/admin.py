from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display=[fields.name for fields in CustomUser._meta.fields]

admin.site.register(CustomUser, CustomUserAdmin)