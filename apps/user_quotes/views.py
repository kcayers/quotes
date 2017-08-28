from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.db.models import Count
from time import strftime

from .models import User, Quote

def index(request):
    return render(request, "user_quotes/index.html")

def register(request):
    if request.method == 'POST':
        result = User.objects.validate_registration(request.POST)
        print result
        if isinstance(result,list):
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['id'] = result
            return redirect('/dashboard')
    else:
        return redirec('/')

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_login(request.POST)
        if isinstance(result, list):
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['id'] = result
            return redirect('/dashboard')
    else:
        return redirect('/')

def home(request):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'all_quotes': Quote.objects.all().exclude(added_by=request.session['id']),
            'favorite_quotes': Quote.objects.filter(added_by=request.session['id']),
            }
    return render(request, "user_quotes/home.html", context)

def create(request):
    if request.method == 'POST':
        result = Quote.objects.validate_quote(request.POST, request.session['id'])
        if isinstance(result, list):
            for error in result:
                messages.error(request, error)
            return redirect('/dashboard')
        else:
            return redirect('/dashboard')

def show_user(request, user_id):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=user_id),
            'quotes': Quote.objects.filter(posted_by=user_id),
            }
    return render(request, "user_quotes/user_show.html", context)

def add(request, quote_id):
    Quote.objects.get(id=quote_id).added_by.add(User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def remove(request, quote_id):
    Quote.objects.get(id=quote_id).added_by.remove(User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
