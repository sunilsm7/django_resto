from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from django.views.generic import (
	CreateView,
	DetailView,
	ListView,
	TemplateView,	
	UpdateView
	)
from django.views.generic.edit import FormView, FormMixin
from django.views.generic.detail import SingleObjectMixin

from comments.forms import CommentForm
from comments.models import Comment

from .forms import (
	RestaurantCreateForm,
	RestaurantLocationCreateForm,
	RestaurantSearchForm
	) 

from .models import RestaurantLocations


# Create your views here.
class RestaurantListView(ListView):
	template_name = 'restaurants/restaurants_list_all.html'
	paginate_by = 10
	form_class = RestaurantSearchForm

	def get_queryset(self):
		query = self.request.GET.get('q')
		queryset = RestaurantLocations.objects.search(query)
		return queryset


class RestaurantDetailView(DetailView, FormView):
	#form_class = CommentForm
	template_name = 'restaurants/restaurantlocations_detail.html'
	queryset = RestaurantLocations.objects.all()
	
	# def get_queryset(self):
	# 	queryset = RestaurantLocations.objects.all()
	# 	return queryset

	def get_context_data(self, **kwargs):
		comments = Comment.objects.filter(object_id=objects.id)
		context = super(RestaurantDetailView, self).get_context_data(**kwargs)
		return context

	def render(self, request):
		objects = get_object_or_404(RestaurantLocations, slug=self.kwargs.get('slug'))
		comments = Comment.objects.filter(object_id=objects.id)
		return render(request, 'restaurants/restaurantlocations_detail.html', {'comment_form': self.form, 'comments':comments, 'object':objects})
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		# initial_data = {
		# 	"content_type": self.object.get_content_type,
		# 	"object_id": self.object.id
		# 	}
		self.form = CommentForm(initial={"content_type": self.object.get_content_type,"object_id": self.object.id})
		return self.render(request)
		#return super(RestaurantDetailView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()

		self.form = CommentForm(request.POST or None)
		form = self.form
		if form.is_valid() and request.user.is_authenticated:
			
			c_type = form.cleaned_data["content_type"]
			content_qs = ContentType.objects.filter(app_label ='restaurants')
			content_type = content_qs.get(model='restaurantlocations')
			obj_id = form.cleaned_data['object_id']
			content_data = form.cleaned_data["content"]
			parent_obj = None

			try:
				parent_id = int(request.POST.get("parent_id"))
			except:
				parent_id = None

			if parent_id:
				parent_qs = Comment.objects.filter(id=parent_id)
				if parent_qs.exists() and parent_qs.count() == 1:
					parent_obj = parent_qs.first()


			new_comment, created = Comment.objects.get_or_create(
								user = request.user,
								content_type= content_type,
								object_id = obj_id,
								content = content_data,
								parent = parent_obj,
							)
			
			return HttpResponseRedirect(new_comment.get_absolute_url())
		else:
			return self.render(request)
			
		#return super(RetaurantComment, self).post(request, *args, **kwargs)


class MyRestaurantListView(LoginRequiredMixin, ListView):
	template_name = 'restaurants/restaurants_list.html'
	paginate_by = 10

	def get_queryset(self):
		return RestaurantLocations.objects.filter(owner=self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'form.html'
	# success_url = '/restaurants/'
	login_url = '/login/'

	def form_valid(self, form):
		instance = form.save(commit=False)
		instance.owner = self.request.user
		return super(RestaurantCreateView, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Add Restaurant'
		return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
	form_class = RestaurantLocationCreateForm
	template_name = 'restaurants/detail-update.html'
	# success_url = '/restaurants/'
	login_url = '/login/'

	def get_context_data(self, *args, **kwargs):
		context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
		name = self.get_object().name
		context['title'] = '{} {}'.format('Update Restaurant: ', name)
		return context

	def get_queryset(self):
		return RestaurantLocations.objects.filter(owner=self.request.user)
