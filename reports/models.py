from django.db import models

# Create your models here.
class Backup(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200, blank=True, null=True) 