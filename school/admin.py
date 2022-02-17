from django.contrib import admin
from .models import School, Student, Classes, Session, Current
# Register your models here.
@admin.register(School)
class schoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'address', 'city', 'pin', 'state', 'country', 'regno')

@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('id', 'school', 'clas', 'class_no')
    
@admin.register(Student)
class studentAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'add_no', 'Class')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'added_date')
    
@admin.register(Current)
class CurrentAdmin(admin.ModelAdmin): 
    list_display = ('id', 'session', 'modified_date')    