from django.contrib import admin

# Register your models here.

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')