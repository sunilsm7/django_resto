from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView


from restaurants.views import (
	RestaurantListView,
    MyRestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    RestaurantUpdateView,
    )
app_name = 'restaurants'

urlpatterns = [
	url(r'^list/$', MyRestaurantListView.as_view(), name='list'),
    url(r'^list/(?P<slug>[\w-]+)/$', RestaurantUpdateView.as_view(), name='detail'),
    url(r'^create/$', RestaurantCreateView.as_view(), name='create'), # RestaurantCreateView.as_view()
	url(r'^$', RestaurantListView.as_view(), name='restaurant'),
    url(r'^(?P<slug>[\w-]+)/$', RestaurantDetailView.as_view(), name='details'),


   
    #url(r'^(?P<slug>[\w-]+)/edit/$', RestaurantUpdateView.as_view(), name='edit'),
]
