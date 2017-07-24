from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView
from django.core.paginator import Paginator

from .forms import ItemForm
from .models import Item

# Create your views here.

class HomeView(View):
	#template_name='home-feed.html'
	paginate_by = 10
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return render(request, 'home.html', {})
		user = request.user
		is_following_user_id = [x.user.id for x in user.is_following.all()]
		qs = Item.objects.filter(user__id__in=is_following_user_id, public=True).order_by("-updated")

		return render(request, 'menus/home-feed.html', {'object_list':qs})
	


class ItemListView(LoginRequiredMixin,ListView):
	template_name = 'menus/item_list.html'
	paginate_by = 10

	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)

class ItemDetailView(LoginRequiredMixin, DetailView):
	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)

class ItemCreateView(LoginRequiredMixin, CreateView):
	form_class = ItemForm
	template_name = 'form.html'

	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemCreateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Create Item'
		return context

	def form_valid(self,form):
		obj = form.save(commit = False)
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
		return Item.objects.filter(user = self.request.user)

	def get_context_data(self, *args, **kwargs):
		context = super(ItemUpdateView, self).get_context_data(*args,**kwargs)
		context['title'] = 'Update Item'
		return context

	def get_form_kwargs(self):
		kwargs = super(ItemUpdateView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs
