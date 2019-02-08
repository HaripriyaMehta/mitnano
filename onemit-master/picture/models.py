from django.db import models

# Create your models here.
class Entry(models.Model):
	name= models.CharField(max_length=100)
	boxNumber= models.IntegerField()
	lineNumber= models.IntegerField()
