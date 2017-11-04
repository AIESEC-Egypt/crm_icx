from django.contrib import admin

# Register your models here.
from .models import *


class ManagerAdmin(admin.ModelAdmin):
    model = Manager
    list_display = (
        '__str__',
        'email',
        'phone',
    )


class ExchangeParticipantAdmin(admin.ModelAdmin):
    model = ExchangeParticipant
    list_display = (
        '__str__',
        'committee',
        'email',
        'phone_number'
    )


admin.site.register(Manager, ManagerAdmin)
admin.site.register(ExchangeParticipant, ExchangeParticipantAdmin)
