from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView


from restaurants.views import (
    #restaurant_listview,
    #restaurant_createview,
    RestaurantListView,
    RestaurantDetailView,
    RestaurantCreateView,
    
    )

urlpatterns = [
    url(r'^$', RestaurantListView.as_view(), name='list'),
    url(r'^create/$', RestaurantCreateView.as_view(), name='create'), # RestaurantCreateView.as_view()
    url(r'^(?P<slug>[\w-]+)/$', RestaurantDetailView.as_view(), name='detail'),
]
