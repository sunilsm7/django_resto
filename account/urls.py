from django.conf.urls import url
from account import views
from django.views.generic import TemplateView

app_name = 'account'
from .views import JoinFormView
urlpatterns = [
	url(r'^validate_username/$', views.validate_username, name='validate_username'), 
	url(r'^join/', JoinFormView.as_view(), name='join'),
	url(r'^$', TemplateView.as_view(template_name='about.html'), name='account'),

]