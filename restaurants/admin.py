from django.contrib import admin
from .models import RestaurantLocations, State, City
# Register your models here.

admin.site.register(State)

admin.site.register(City)

class RestaurantLocationsAdmin(admin.ModelAdmin):
	list_display = ['name', 'city','location', 'category','updated']
	list_filter = ['location', 'category']
	
admin.site.register(RestaurantLocations, RestaurantLocationsAdmin)