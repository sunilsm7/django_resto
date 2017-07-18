from django.db.models import Q 
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from .models import RestaurantLocations

# Create your views here.

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




    