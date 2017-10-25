from django.contrib import admin
from .models import *

# Register your models here.

class ProgramTypeAdmin(admin.ModelAdmin):
    model = ProgramType
    list_display = (
        'id',
        'title',
    )


class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('id','__str__', 'status')


admin.site.register(ProgramType, ProgramTypeAdmin)
admin.site.register(Opportunity, OpportunityAdmin)

