from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q 
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
from .models import RestaurantLocations



# Create your views here.
@login_required()
def restaurant_createview(request):
    form = RestaurantLocationCreateForm(request.POST or None)
    errors  = None
    if form.is_valid():
        if request.user.is_authenticated():
            instance = form.save(commit = False)
            instance.owner = request.user
            instance.save()
            # customize 
            # like a pre save
            #form.save()
            # like a post save
            return HttpResponseRedirect("/restaurants")
        else:
            return HttpResponseRedirect("/login")
        if form.errors:
            errors = form.errors

    template_name = 'restaurants/form.html'
    context = {'form':form, 'errors':errors}
    return render(request, template_name, context)


def restaurant_listview(request):
    template_name = 'restaurants/restaurants_list.html'
    queryset = RestaurantLocations.objects.all()
    context = {
    "object_list":queryset,
    }
    return render(request, template_name, context)

class RestaurantListView(ListView):
    template_name = 'restaurants/restaurants_list.html'

    def get_queryset(self):
        
        slug =self.kwargs.get("slug")
        if slug:
            queryset = RestaurantLocations.objects.filter(
                Q(category__iexact=slug) |
                Q(category__icontains=slug)
                )
        else:
            queryset = RestaurantLocations.objects.all()
        return queryset


class RestaurantDetailView(DetailView):
    #template_name = 'restaurants/restaurants_list.html'
    queryset = RestaurantLocations.objects.all()


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




    