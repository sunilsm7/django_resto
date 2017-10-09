from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import (
	View,
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)

from django.views.generic.edit import FormView, FormMixin

from .forms import ItemForm
from comments.forms import CommentForm
from comments.models import Comment

from .models import Item
from restaurants.models import RestaurantLocations


# Create your views here.

class HomeView(ListView):
	# template_name='home-feed.html'
	paginate_by = 10

	# def get_queryset(self):
	# 	query = self.request.GET.get('q')
	# 	querset = RestaurantLocations.objects.search(query)
	# 	return querset

	def get(self, request, *args, **kwargs):
		if request.user.is_authenticated():
			user = request.user
			is_following_user_id = [x.user.id for x in user.is_following.all()]
			qs = Item.objects.filter(user__id__in=is_following_user_id, public=True).order_by("-updated")
			return render(request, 'menus/home-feed.html', {'object_list': qs})
		else:
			context = {}
			# if 'q' in self.request.GET:
			#     query = self.request.GET.get('q')
			#     qs = RestaurantLocations.objects.search(query)
			#     if qs.exists():
			#         context['locations'] = qs
			#         return render(request, 'search_results.html', context)
			return render(request, 'home.html', context)


class ItemListView(ListView):
	template_name = 'menus/item_list_all.html'
	paginate_by = 10

	def get_queryset(self):
		query = self.request.GET.get('q')
		querset = Item.objects.filter(public=True).search(query)
		return querset


class MyItemListView(LoginRequiredMixin, ListView):
	template_name = 'menus/item_list.html'
	paginate_by = 10

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)


class ItemDetailView(DetailView, FormView):
	def get_queryset(self):
		return Item.objects.filter(public=True)

	def get_context_data(self, **kwargs):
		comments = Comment.objects.filter(object_id=objects.id)
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		return context

	def render(self, request):
		objects = get_object_or_404(Item, pk=self.kwargs.get('pk'))
		comments = Comment.objects.filter(object_id=objects.id)
		return render(request, 'menus/item_detail.html', {'comment_form': self.form, 'comments':comments, 'object':objects})
	
	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		# initial_data = {
		# 	"content_type": self.object.get_content_type,
		# 	"object_id": self.object.id
		# 	}
		self.form = CommentForm(initial={"content_type": self.object.get_content_type,"object_id": self.object.id})
		return self.render(request)
		#return super(ItemDetailView, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()

		self.form = CommentForm(request.POST or None)
		form = self.form
		if form.is_valid() and request.user.is_authenticated:
			
			c_type = form.cleaned_data["content_type"]
			#content_qs = ContentType.objects.filter(app_label ='restaurants')
			content_type = ContentType.objects.get(app_label="menus", model="item")
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


class ItemCreateView(LoginRequiredMixin, CreateView):
	form_class = ItemForm
	template_name = 'form.html'

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Create Item'
		return context

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		return super(ItemCreateView, self).form_valid(form)

	def get_form_kwargs(self):
		kwargs = super(ItemCreateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs


class ItemUpdateView(LoginRequiredMixin, UpdateView):
	form_class = ItemForm
	template_name = 'menus/detail-update.html'

	def get_queryset(self):
		return Item.objects.filter(user=self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update Item'
		return context

	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
