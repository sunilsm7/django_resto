from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

from restaurants.models import RestaurantLocations
# Create your models here.

class Item(models.Model):
	# associations
	user 		= models.ForeignKey(settings.AUTH_USER_MODEL) # class_instance.model_set.all()
	restaurant 	= models.ForeignKey(RestaurantLocations)
	#item stuff
	name 		= models.CharField(max_length = 128) 
	contents 	= models.TextField(help_text = 'Separate each item by comma')
	excludes 	= models.TextField(blank = True, null = True, help_text = 'Separate each item by comma')
	public		= models.BooleanField(default = True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)  

	class Meta:
		ordering = ['-updated', '-timestamp']

	def get_absolute_url(self):
		return reverse('menus:detail', kwargs= {'pk': self.pk})

	def get_contents(self):
		return self.contents.split(",")

	def get_excludes(self):
		return self.excludes.split(",")

