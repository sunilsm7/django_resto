from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, View
# Create your views here.

def validate_username(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
        email    = request.GET.get('email', None)
        pasword    = request.GET.get('pasword', None)
        
        data = {
            'username_is_taken':User.objects.filter(username__iexact=username).exists(),
            'email_is_taken':User.objects.filter(email__iexact=email).exists(),
        }
        if data['username_is_taken']:
            data['error_message'] = 'username not available.'
        elif data['email_is_taken']:
            data['error_message_email'] = 'email id not available.'
        return JsonResponse(data)

