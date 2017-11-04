from django.contrib import admin
from .models import *


# Register your models here.


class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value')


class CommitteeAdmin(admin.ModelAdmin):
    model = Committee
    list_display = (
        '__str__',
        'id',
        'get_mc',
    )
    list_filter = (
        'entity_type',
    )
    search_fields = (
        'parent_committee__name',
    )

    def get_mc(self, obj):
        if (obj.parent_committee != None):
            return obj.parent_committee.name
        else:
            return 'No Parent'

    get_mc.short_description = 'MC'  # Renames column head


class APIRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'current_page', 'total_pages')


admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(Committee, CommitteeAdmin)
admin.site.register(APIRequest, APIRequestAdmin)
