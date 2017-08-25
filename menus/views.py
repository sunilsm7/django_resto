from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, ListView, DetailView, UpdateView, CreateView

from .forms import ItemForm
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
            if 'q' in self.request.GET:
                query = self.request.GET.get('q')
                qs = RestaurantLocations.objects.search(query)
                if qs.exists():
                    context['locations'] = qs
                    return render(request, 'search_results.html', context)
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


class ItemDetailView(DetailView):
    def get_queryset(self):
        return Item.objects.filter(public=True)


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
