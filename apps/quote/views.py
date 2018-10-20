# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from ..login.models import User
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib import messages

# Create your views here.
def index(request):
    context = {
        'poster': User.objects.get(id=request.session['user_id']),
        'favorites': Favorite.objects.filter(poster = User.objects.get(id=request.session['user_id'])),
        'quotes': Quote.objects.all().filter(id=request.session['user_id']),

    }
    return render(request, 'quote/index.html', context)

def create(request):
    errs = Quote.objects.validate_quote(request.POST)
    if errs:
        for e in errs:
            messages.error(request, e)
            return HttpResponseRedirect(reverse('quote:index'))
    else:
        poster = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.create(quote=request.POST['quote'], poster = poster, author= request.POST['author'])
        return HttpResponseRedirect(reverse('quote:index'))

def favorite_add(request, quote_id):
    poster = User.objects.get(id=request.session['user_id'])
    quote = Quote.objects.get(id=quote_id)
    Favorite.objects.create(quote = quote, poster = poster)
    return redirect('quote:index')

def show_user(request, user_id, ):
    poster = User.objects.get(id=user_id)
    # author = Quote.objects.get(id=quote_id)
    context = {
        # 'author' : Quote.objects.filter(author = author),
        'quotes': Quote.objects.filter(poster = poster),
        'poster' : poster,
    }
    return render(request, 'quote/show.html', context)

def delete_quote(request, quote_id):
    fave = Favorite.objects.get(quote = Quote.objects.get(id=quote_id))
    fave.delete()
    return redirect('quote:index')