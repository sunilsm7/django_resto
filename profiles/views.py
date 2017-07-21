from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View

from .forms import RegisterForm

from menus.models import Item
from restaurants.models import RestaurantLocations	

from .models import Profile
# Create your views here.
 
User =get_user_model()

class RegisterView(CreateView):
	form_class = RegisterForm
	template_name ='registration/register.html'
	success_url = '/'

	def dispatch(self, *args, **kwargs):
		# if self.request.user.is_authenticated():
		# 	return redirect('/login')
		return super(RegisterView, self).dispatch(*args,**kwargs)

class ProfileFollowToggle(LoginRequiredMixin, View):
	def post(sel, request, *args, **kwargs):
		username_to_toggle =request.POST.get("username")
		profile_, is_following = Profile.objects.toggle_follow(request.user,username_to_toggle )
		return redirect('/u/{}'.format(profile_.user.username))


class ProfileDetailView(DetailView):
	template_name = 'profiles/user_detail.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User,username__iexact=username, is_active=True)

	def get_context_data(self, *args, **kwargs):
		context = super(ProfileDetailView,self).get_context_data(*args,**kwargs)
		user = context['user']
		is_following = False
		if user.profile in self.request.user.is_following.all():
			is_following = True
		context['is_following'] = is_following
		query = self.request.GET.get('q')
		items_exists = Item.objects.filter(user=user).exists()
		qs = RestaurantLocations.objects.filter(owner=user).search(query)
		if items_exists and qs.exists():
			context['locations'] = qs
		return context	