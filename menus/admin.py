from django.contrib import admin

from .models import Item, ItemCategory
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
	list_display = ['name', 'restaurant']
	list_filter = ['user', 'restaurant']
	list_per_page = 20
	
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCategory)
