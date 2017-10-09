from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.db.models import Q

from comments.models import Comment
from .utils import unique_slug_generator
from .validators import validate_category
# Create your models here.
User = settings.AUTH_USER_MODEL

class RestaurantLocationsQuerySet(models.query.QuerySet):
	def search(self, query): # RestaurantLocations.objects.all().search(query) or  RestaurantLocations.objects.all().filter(something).search(query)
		if query:
			query = query.strip()
			return self.filter(
				Q(name__icontains=query)|
				Q(city__city_name__iexact=query)|
				Q(location__icontains=query)|
				Q(location__iexact=query)|
				Q(category__cuisine__icontains=query)|
				Q(category__cuisine__iexact=query)|
				Q(item__name__icontains=query)|
				Q(item__item_category__category__istartswith=query)
				).distinct()

		return self
		


class RestaurantLocationsManager(models.Manager):
	def get_queryset(self):
		return RestaurantLocationsQuerySet(self.model, using=self._db)

	def search(self, query): # RestaurantLocations.objects.search()
		return self.get_queryset().search(query)

class State(models.Model):
	state_name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "01 Restaurant States"

	def __str__(self):
		return '{}'.format(self.state_name)


class City(models.Model):
	city_name 	= models.CharField(max_length=200)
	state 		= models.ForeignKey(State)

	class Meta:
		verbose_name_plural = "02 Restaurant City"

	def __str__(self):
		return '{} {}'.format(self.city_name, self.state)

class RestaurantCuisine(models.Model):
	cuisine 	= models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = "03 Restaurant Cuisine"

	def __str__(self):
		return '{}'.format(self.cuisine)

class RestaurantLocations(models.Model):
	owner 		= models.ForeignKey(User) # class_instance.model_set.all()
	name 		= models.CharField(max_length=128)
	city 		= models.ForeignKey(City)
	location 	= models.CharField(max_length=128, null=True, blank=True)
	category 	= models.ForeignKey(RestaurantCuisine, null=True, blank=True)
	#overview	= models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)   
	slug		= models.SlugField(null=True, blank=True)

	objects = RestaurantLocationsManager()

	class Meta:
		ordering = ['-updated']
		verbose_name_plural = "04 Restaurant Location"
		permissions = (
				('can_view', 'Can View'),
				('can_modify', 'Can Modify'),
			)

	def __str__(self):
		return '{} {}'.format(self.name, self.location)

	def get_absolute_url(self):
		return reverse('restaurants:detail', kwargs= {'slug': self.slug})
		
	@property	
	def title(self):
		return self.name

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type 
	
	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

class RestaurantHighlights(models.Model):
	CHOICES = (
		("available","available"),
		("not available","not available"),
	)
	AC_CHOICES = (
		("accepted","accepted"),
		("not accepted","not accepted"),
	)
	restaurant 		= models.ForeignKey(RestaurantLocations)
	car_parking 	= models.CharField(max_length=128, null=True, blank=True,choices=CHOICES)
	home_delivery	= models.CharField(max_length=128, null=True, blank=True,choices=CHOICES)
	take_away		= models.CharField(max_length=128, null=True, blank=True,choices=CHOICES)
	cards			= models.CharField(max_length=128, null=True, blank=True,choices=AC_CHOICES)
	ac				= models.CharField(max_length=128, null=True, blank=True,choices=CHOICES)

	class Meta:
		verbose_name_plural = "05 Restaurant Details"

	def __str__(self):
		return '{} {}'.format(self.restaurant, self.ac)


def rl_pre_save_receiver(sender, instance, *args, **kwargs):

	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=RestaurantLocations)

