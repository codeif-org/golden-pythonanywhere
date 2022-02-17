from django.contrib import admin
from reports.models import *

# Register your models here.
@admin.register(Backup)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'comment') 