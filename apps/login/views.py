# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from ..quote.models import Quote
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Registration successful!")
    return HttpResponseRedirect(reverse('quote:index'))

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    messages.success(request, "Login successful!")
    return HttpResponseRedirect(reverse('quote:index'))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


def show(request, user_id):
    user = User.objects.get(id=user_id)
    unique_ids = user.quotes_left.all().values("quote").distinct()
    unique_quotes = []
    for quote in unique_ids:
        unique_quotes.append(Quote.objects.get(id=quote['quote']))
    context = {
        'user': user,
        'unique_quotes': unique_quotes
    }
    return render(request, 'login/show.html', context)