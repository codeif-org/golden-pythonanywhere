from django.db import models
from django.contrib.auth.models import User
# from sqlalchemy import null

# Create your models here.
class School(models.Model):
    school = models.CharField(max_length=200, default='', blank=False, null=False)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pin = models.IntegerField()
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    regno = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Session(models.Model):    
    session = models.CharField(max_length=50, unique=True)
    added_date = models.DateField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.PROTECT, default=1) 
    
class Current(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(auto_now=True)      

class Classes(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    clas = models.CharField(max_length=30)
    class_no = models.IntegerField(null=True, blank=True)  

class Student(models.Model):
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50, blank=True, null=True)
    lname = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fathername = models.CharField(max_length=70)
    mothername = models.CharField(max_length=70, blank=True, null=True)
    fatherphone = models.IntegerField(blank=True, null=True)
    fatheremail = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    add_no = models.CharField(max_length=50)
    roll_no = models.CharField(max_length=5, blank=True, null=True) 
    dob = models.DateField(blank=True, null=True)
    added_date = models.DateField(auto_now_add=True, blank=True, null=True)
    modified_date = models.DateField(auto_now=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    religion = models.CharField(max_length=15, blank=True, null=True)
    category = models.CharField(max_length=15, blank=True, null=True)
    Class = models.ForeignKey(Classes, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.PROTECT, default=1)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, default=1) 
    
  