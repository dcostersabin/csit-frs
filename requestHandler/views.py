from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


# indexpage
def index(request):
    return render(request, 'index/index.html')


@login_required
def home(request):
    return render(request, 'home/home.html')
