from django.contrib import admin
from .models import RestaurantLocations, State, City,RestaurantCuisine,RestaurantHighlights
# Register your models here.

admin.site.register(State)

admin.site.register(City)
admin.site.register(RestaurantCuisine)
admin.site.register(RestaurantHighlights)

class RestaurantLocationsAdmin(admin.ModelAdmin):
	list_display = ['name', 'city','location', 'category','updated']
	list_filter = ['location', 'category']
	
admin.site.register(RestaurantLocations, RestaurantLocationsAdmin)