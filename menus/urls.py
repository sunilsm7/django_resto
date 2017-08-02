from django.conf.urls import url
from django.contrib import admin

from .views import (
    MyItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView
    )

app_name = 'menus'

urlpatterns = [
    url(r'^$', MyItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'), # RestaurantCreateView.as_view()
    url(r'^(?P<pk>\d+)/$', ItemUpdateView.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/edit/$', ItemUpdateView.as_view(), name='edit'),
]
