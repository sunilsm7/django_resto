from django.conf.urls import url
from django.contrib import admin

from .views import (
	ItemListView,
    MyItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView
    )

app_name = 'menus'

urlpatterns = [
	
    url(r'^list/$', MyItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'), # RestaurantCreateView.as_view()
    url(r'^list/(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),
    url(r'^$', ItemListView.as_view(), name='items'),
    url(r'^(?P<pk>\d+)/details/$', ItemDetailView.as_view(), name='details'),
]
