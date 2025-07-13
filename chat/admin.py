from django.contrib import admin

from chat.models import PrivateMessage


# Register your models here.

@admin.register(PrivateMessage)
class ModelNameAdmin(admin.ModelAdmin):
    pass