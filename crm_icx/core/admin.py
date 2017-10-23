from django.contrib import admin
from .models import *


# Register your models here.

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value')


admin.site.register(AccessToken, AccessTokenAdmin)


class APIRequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'current_page', 'total_pages')


admin.site.register(APIRequest, APIRequestAdmin)
