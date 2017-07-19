from django.db.models import Q 
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import RestaurantLocations
from .forms import RestaurantCreateForm, RestaurantLocationCreateForm
# Create your views here.

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


class RestaurantCreateView(CreateView):
    form_class = RestaurantLocationCreateForm
    template_name = 'restaurants/form.html'
    success_url = '/restaurants/'



    