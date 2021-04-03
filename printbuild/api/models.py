from django.db import models
from django.db.models.signals import post_save
from .gen import *

# Create your models here.

class Spare(models.Model):
    spare = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    transNo = models.IntegerField(max_length=100)


class Spareprint(models.Model):
    transno = models.IntegerField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=True)

# signals

def save_post(sender,instance,**kwargs):
    lasttrans = Spareprint.objects.order_by('-pk')[0]
    transno = lasttrans.transno
    generatePDF(str(transno))

post_save.connect(save_post,sender=Spareprint)
