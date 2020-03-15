from django.urls import path,include
from . import views as views

urlpatterns =[
path('', views.index,name='index'),
path('home/',views.home,name='home'),
path('add_user/',views.add_user,name='addUser'),
path('capture/', views.capture, name="capture"),
path('train/',views.train_data, name="train"),
path('recognize/',views.rec,name="recognize"),
path('users/',views.show_users,name='users'),
    path('addMoreData/',views.add_more_data,name='addMoreData'),
    path('adminTest/',views.admin_test,name='adminTest'),
    path('profile/',views.view_profile,name='profile'),
    path('search/',views.search,name='search'),
    path('attend/',views.attend,name='attend'),
]
