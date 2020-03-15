from django.urls import path,include
from . import views as views

urlpatterns =[
path('', views.index,name='index'),
path('home/',views.home,name='home'),
]
