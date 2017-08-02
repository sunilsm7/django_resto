from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from restaurants.models import RestaurantLocations
# Create your models here.

class ItemQuerySet(models.query.QuerySet):
	def search(self, query): # RestaurantLocations.objects.all().search(query) or  RestaurantLocations.objects.all().filter(something).search(query)
		if query:
			query = query.strip()
			return self.filter(
				Q(name__icontains=query)|
				Q(item_category__category__istartswith=query)
				#Q(restaurant_id__name__icontains=query)
				# Q(course__icontains=query)|
				# Q(contents__icontains=query)
				).distinct()
		return self

class ItemManager(models.Manager):
	def get_queryset(self):
		return ItemQuerySet(self.model, using=self._db)

	def search(self, query): # RestaurantLocations.objects.search()
		return self.get_queryset().search(query)

class ItemCategory(models.Model):
	category = models.CharField(max_length = 128) 
	class Meta:
		verbose_name_plural = "01 Menu Item Category"

	def __str__(self):
		return '{}'.format(self.category)

class Item(models.Model):
	COURSE_CHOICES = (
		("All","All"),
		("Main Course","Main Course"),
		("Side Dish","Side Dish"),
		("Drinks","Drinks"),
		("Juice","Juice"),
		("Snacks","Snacks"),
		("Ice Creams","Ice Creams"),
	)
	# associations
	user 			= models.ForeignKey(settings.AUTH_USER_MODEL) # class_instance.model_set.all()
	restaurant 		= models.ForeignKey(RestaurantLocations)
	#item stuff
	name 			= models.CharField(max_length = 128) 
	item_category 	= models.ForeignKey(ItemCategory)
	course			= models.CharField(max_length=50,blank=True, null=True, choices=COURSE_CHOICES, default="All")
	contents 		= models.TextField(help_text = 'Separate each item by comma')
	excludes 		= models.TextField(blank = True, null = True, help_text = 'Separate each item by comma')
	public			= models.BooleanField(default = True)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True) 

	objects = ItemManager()

	def __str__(self) :
		return '{} {}'.format(self.name, self.restaurant)

	class Meta:
		ordering = ['-updated', '-timestamp']
		verbose_name_plural = "02 Menu Item"

	def get_absolute_url(self):
		return reverse('menus:detail', kwargs= {'pk': self.pk})

	def get_contents(self):
		return self.contents.split(",")

	def get_excludes(self):
		return self.excludes.split(",")

