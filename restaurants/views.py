from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocations

# Create your views here.
class RestaurantListView(ListView):
    template_name = 'restaurants/restaurants_list_all.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = RestaurantLocations.objects.search(query) 
        return queryset

    # def get(self, request, *args, **kwargs):
    #     context = {}
    #     query = self.request.GET.get('q')
    #     qs = RestaurantLocations.objects.search(query)  
    #     if qs.exists():
    #         context['object_list'] = qs
    #         return render(request, 'restaurants/restaurants_list_all.html', context)
    #     return render(request, 'restaurants/restaurants_list_all.html', {'object_list':object_list})

class RestaurantDetailView(DetailView):
    #template_name = 'restaurants/restaurants_list.html'
    queryset = RestaurantLocations.objects.all()

    # def get_queryset(self):
    #     return RestaurantLocations.objects.filter(owner = self.request.user)

class MyRestaurantListView(LoginRequiredMixin, ListView):
    template_name = 'restaurants/restaurants_list.html'
    paginate_by = 10

    def get_queryset(self):
        return RestaurantLocations.objects.filter(owner = self.request.user)

# class RestaurantDetailView(LoginRequiredMixin, DetailView):
#     #template_name = 'restaurants/restaurants_list.html'
#     #queryset = RestaurantLocations.objects.all()

#     def get_queryset(self):
#         return RestaurantLocations.objects.filter(owner = self.request.user)


class RestaurantCreateView(LoginRequiredMixin, CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'form.html'
    #success_url = '/restaurants/'
    login_url = '/login/'

    def form_valid(self, form):
        instance = form.save(commit = False)
        instance.owner = self.request.user
        return super(RestaurantCreateView,self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Restaurant'
        return context


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/detail-update.html'
    #success_url = '/restaurants/'
    login_url = '/login/'

    def get_context_data(self, *args, **kwargs):
        context = super(RestaurantUpdateView, self).get_context_data(*args, **kwargs)
        name = self.get_object().name
        context['title'] = '{} {}'.format('Update Restaurant: ',name)
        return context

    def get_queryset(self):
        return RestaurantLocations.objects.filter(owner = self.request.user)