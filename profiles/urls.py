from django.conf.urls import url

from .views import (
    ProfileDetailView,
    
    )
from profiles import views
app_name = 'profiles'
urlpatterns = [
    url(r'^search/',views.SearchView.as_view(), name='search'),
    url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name='detail'),  
    
]
