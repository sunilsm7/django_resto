from django.contrib import admin
from .models import RestaurantLocations
# Register your models here.

class RestaurantLocationsAdmin(admin.ModelAdmin):
	list_display = ['name', 'location', 'category']
	list_filter = ['location', 'category']
	
admin.site.register(RestaurantLocations, RestaurantLocationsAdmin)