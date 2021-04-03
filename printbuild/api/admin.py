from django.contrib import admin
from .models import *

# Register your models here.

class SpareAdmin(admin.ModelAdmin):
    list_display = ('id','spare','transNo','status',)
    list_display_links = ('id','spare','transNo',)

admin.site.register(Spare,SpareAdmin)
