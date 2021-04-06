from django.contrib import admin
from .models import *

# Register your models here.

class SpareAdmin(admin.ModelAdmin):
    list_display = ('id','spare','transNo','status',)
    list_display_links = ('id','spare','transNo',)

class PartAdmin(admin.ModelAdmin):
    list_display = ('id','partname')

admin.site.register(Spare,SpareAdmin)
admin.site.register(Part,PartAdmin)
admin.site.register(Spareprint)
