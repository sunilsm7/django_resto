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
        user = authenticate(username='username', password='pasword')
        
        if user is not None:
            valid_login = True
        else:
            valid_login = False
        data = {
            'username_is_taken':User.objects.filter(username__iexact=username).exists(),
            'email_is_taken':User.objects.filter(email__iexact=email).exists(),
            'user_login' : valid_login,
        }
        if data['username_is_taken']:
            data['error_message'] = 'username not available.'
        elif data['email_is_taken']:
            data['error_message_email'] = 'email id not available.'
        elif data['user_login']:
            data['error_message_login'] = 'invalid password.'
        return JsonResponse(data)

