"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Event(models.Model):
	hashString = models.CharField(max_length = 200)
	adminHashString = models.CharField(max_length = 200)
	name = models.CharField(max_length = 30)
	organizer = models.CharField(max_length = 30)
	admin = models.CharField(max_length = 30)
	total = models.DecimalField(max_digits = 6, decimal_places = 2)
	desc = models.TextField(null=True)
	goal = models.IntegerField()
	date = models.DateField()
	email = models.EmailField()
	
	def __unicode__(self):
		return self.hashString+" "+self.name

class Contributor(models.Model):
	event = models.ForeignKey(Event)
	name = models.CharField(max_length = 30)
	money = models.DecimalField(max_digits = 6, decimal_places = 2)
		
