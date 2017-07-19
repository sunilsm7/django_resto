from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .forms import ItemForm
from .models import Item
# Create your views here.

class ItemListView(ListView):
	template_class = 'menus/item_list.html'
	def get_queryset(self):
		return Item.objects.filter(user = self.request.user)

class ItemDetailView(DetailView):
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
	template_name = 'form.html'

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
