from django.db import models


# Create your models here.

class AudioModel(models.Model):
    aid = models.CharField(max_length=30, null=False, primary_key=True)
    name = models.CharField(max_length=30)
