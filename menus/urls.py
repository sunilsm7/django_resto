from django.conf.urls import url
from django.contrib import admin

from .views import (
    ItemListView,
    ItemDetailView,
    ItemCreateView,
    ItemUpdateView
    )

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='list'),
    url(r'^create/$', ItemCreateView.as_view(), name='create'), # RestaurantCreateView.as_view()
    url(r'^(?P<pk>\d+)/$', ItemDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/edit/$', ItemUpdateView.as_view(), name='edit'),
]
