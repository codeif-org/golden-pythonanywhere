from django.contrib import admin
from fee.models import *

# Register your models here.
@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'month', 'month_no', 'start_date', 'end_date')
    
@admin.register(FeeStruct)
class FeeStructAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_type', 'month', 'clas', 'amount')  

@admin.register(FeeSubmit)
class FeeSubmitAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'submit_date', 'mop')

@admin.register(DeletedFeeSubmit)
class DeletedFeeSubmitAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'submit_date', 'mop')

@admin.register(FeeAdvance)
class FeeAdvanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'advance', 'date')

@admin.register(FeeConcession)
class FeeConcession(admin.ModelAdmin):
    list_display = ('id', 'student', 'fee_submit', 'concession_type', 'reason', 'date')
    
@admin.register(FeeStructByMonth)
class FeeStructByMonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'clas', 'month', 'amount')    
    
@admin.register(FeeSubmitByMonth)
class FeeSubmitByMonthAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'month_no', 'session_fee_submitted', 'date')    
    
@admin.register(ChequeDetails)
class ChequeDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_submit', 'cheque_no', 'issued_by', 'bank', 'issue_date') 
    
@admin.register(DeletedChequeDetails)
class DeletedChequeDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_submit', 'cheque_no', 'issued_by', 'bank', 'issue_date')           
    
@admin.register(OnlineNeftDetails)
class OnlineNeftDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_submit', 'utr_no', 'pay_by', 'pay_date')  
    
@admin.register(DeletedOnlineNeftDetails)
class DeletedOnlineNeftDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fee_submit', 'utr_no', 'pay_by', 'pay_date')           
    
@admin.register(MiscFee)
class MiscFeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'fee_type', 'amount', 'reason', 'date')       