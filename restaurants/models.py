from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
# Create your models here.

class RestaurantLocations(models.Model):
	name 		= models.CharField(max_length=128)
	location 	= models.CharField(max_length=128, null=True, blank=True)
	category 	= models.CharField(max_length=128, null=True, blank=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)   
	slug		= models.SlugField(null=True, blank=True)

	class Meta:
		ordering = ['-updated']
		verbose_name_plural = "Restaurant Location"

	def __str__(self):
		return '{} {}'.format(self.name, self.location)

	@property	
	def title(self):
		return self.name 


def rl_pre_save_receiver(sender, instance, *args, **kwargs):
		if not instance.slug:
			instance.slug = unique_slug_generator(instance)

# def rl_post_save_receiver(sender, instance, created, *args, **kwargs):
# 	print('saved...')
# 	print(instance.timestamp)
# 	if not instance.slug:
# 		instance.slug = unique_slug_generator(instance)
	
pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocations)

#post_save.connect(rl_post_save_receiver, sender=RestaurantLocations)	