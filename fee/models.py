from socket import NI_NUMERICHOST
from django.db import models
import datetime

# Create your models here.
class Month(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.PROTECT, null=True, blank=True)
    month = models.CharField(max_length=50)
    month_no = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True) 
    due_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.month
    
class FeeStructByMonth(models.Model):
    school = models.ForeignKey('school.School', on_delete=models.PROTECT, null=True, blank=True)
    clas = models.ForeignKey('school.Classes', on_delete=models.CASCADE) 
    month = models.ForeignKey('fee.Month', on_delete=models.CASCADE) 
    amount = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)
    
    # def __str__(self):
    #     return self.clas.clas    

class FeeStruct(models.Model):
    fee_type = models.CharField(max_length=100)
    month = models.ForeignKey('fee.Month', on_delete=models.CASCADE) 
    clas = models.ForeignKey('school.Classes', on_delete=models.PROTECT)
    amount = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.fee_type + ' - ' + str(self.month) + ' - ' + str(self.clas)


# class FeeStruct(models.Model):
#     school = models.ForeignKey('school.School', on_delete=models.PROTECT, null=True, blank=True)
#     month = models.ForeignKey('fee.Month', on_delete=models.PROTECT, null=True, blank=True)
#     student = models.ForeignKey('school.Student', on_delete=models.PROTECT, null=True, blank=True)
#     amount = models.IntegerField()
#     paid_amount = models.IntegerField(null=True, blank=True)
#     due_amount = models.IntegerField(null=True, blank=True)
#     paid_date = models.DateField(null=True, blank=True)
#     due_date = models.DateField(null=True, blank=True)
#     paid_status = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.student.fname

class FeeSubmit(models.Model):
    student = models.ForeignKey('school.student', on_delete=models.CASCADE)
    txn_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)
    submit_date = models.DateField()
    mop = models.CharField(max_length=50, default='Cash')
    memo_no = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)
    
class MiscFee(models.Model):
    student = models.ForeignKey('school.Student', on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=100)
    amount = models.IntegerField()
    reason = models.TextField(null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(default=0) 
    date = models.DateField(auto_now=True)
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)    

class DeletedFeeSubmit(models.Model):
    student = models.ForeignKey('school.student', on_delete=models.CASCADE)
    txn_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.IntegerField()
    delete_date = models.DateField(auto_now=True)
    submit_date = models.DateField()
    mop = models.CharField(max_length=50, default='Cash')
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)
    
class FeeSubmitByMonth(models.Model):
    student = models.OneToOneField('school.student', on_delete=models.CASCADE)
    month_no = models.IntegerField(default=0)
    advanced_amount = models.IntegerField(default=0)
    total_session_fee = models.IntegerField(default=0)
    session_fee_submitted = models.IntegerField(default=0)
    session_fee_left = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)
    session = models.ForeignKey('school.Session', on_delete=models.CASCADE, default=1)

class FeeAdvance(models.Model):
    student = models.ForeignKey('school.student', on_delete=models.CASCADE)
    advance = models.IntegerField()
    date = models.DateField(auto_now=True)
    # mop = models.CharField(max_length=50, default='Cash')

class FeeConcession(models.Model):
    fee_submit = models.OneToOneField(FeeSubmit, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('school.student', on_delete=models.CASCADE)
    concession_type = models.CharField(max_length=50, default='None')
    reason = models.TextField()
    date = models.DateField(auto_now=True)
    
class ChequeDetails(models.Model):
    fee_submit = models.OneToOneField(FeeSubmit, related_name='fee_cheque', on_delete=models.CASCADE)
    cheque_no = models.CharField(max_length=50, null=True, blank=True)
    issued_by = models.CharField(max_length=100, null=True, blank=True)
    bank = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    issue_date = models.DateField()
    
class DeletedChequeDetails(models.Model):
    fee_submit = models.OneToOneField(DeletedFeeSubmit, related_name='fee_cheque', on_delete=models.CASCADE) 
    cheque_no = models.CharField(max_length=50, null=True, blank=True)
    issued_by = models.CharField(max_length=100, null=True, blank=True) 
    bank = models.CharField(max_length=50, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    issue_date = models.DateField()        
    
class OnlineNeftDetails(models.Model):
    fee_submit = models.OneToOneField(FeeSubmit, related_name='fee_online', on_delete=models.CASCADE)
    utr_no = models.CharField(max_length=50, null=True, blank=True)
    pay_by = models.CharField(max_length=50, null=True, blank=True)
    pay_date = models.DateField()
    
class DeletedOnlineNeftDetails(models.Model):
    fee_submit = models.OneToOneField(DeletedFeeSubmit, related_name='fee_online', on_delete=models.CASCADE)
    utr_no = models.CharField(max_length=50, null=True, blank=True)
    pay_by = models.CharField(max_length=50, null=True, blank=True) 
    pay_date = models.DateField()    
             