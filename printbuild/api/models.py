from django.db import models

# Create your models here.

class Spare(models.Model):
    spare = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    transNo = models.IntegerField(max_length=100)

