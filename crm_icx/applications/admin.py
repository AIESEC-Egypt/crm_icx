from django.contrib import admin

# Register your models here.
from django.contrib.admin import DateFieldListFilter

from .models import *


class ApplicationAdmin(admin.ModelAdmin):
    model = Application
    list_display = (
        'id',
        'exchange_participant',
        'get_ep_id',
        'get_lc',
        'get_mc',
        'get_ep_email',
        'status',
        'date_approved',
        'date_realized',
        'created_at',
        'updated_at',
        'experience_start_date',
    )
    list_filter = (
        'status',
        ('created_at', DateFieldListFilter),
    )
    search_fields = (
        'status',
    )

    # readonly_fields = ('created_at',)
    def get_ep_id(self, obj):
        return obj.exchange_participant.id

    def get_ep_email(self, obj):
        return obj.exchange_participant.email

    def get_lc(self, obj):
        return obj.exchange_participant.committee

    def get_mc(self, obj):
        if (obj.exchange_participant.committee.parent_committee != None):
            return obj.exchange_participant.committee.parent_committee.name
        else:
            return 'No Parent'

    get_ep_id.short_description = 'EP ID'  # Renames column head
    get_ep_email.short_description = 'Email'  # Renames column head
    get_lc.short_description = 'Home LC'  # Renames column head
    get_mc.short_description = 'Home MC'  # Renames column head




admin.site.register(Application, ApplicationAdmin)
