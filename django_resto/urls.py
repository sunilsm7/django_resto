from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
    )
from menus.views import HomeView
#from profiles.views import ProfileFollowToggle,RegisterView
from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset_done/$',PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^u/', include('profiles.urls', namespace='profiles')),
    url(r'^items/', include('menus.urls', namespace='menus')),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

