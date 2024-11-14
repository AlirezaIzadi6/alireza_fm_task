from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def index(request):
    return render(request, 'index.html', {'context': {}})
