
from django.contrib import admin
from django.urls import path,include
from flyhigh import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flights/', views.flights, name='flights'),
    path('filter/',views.filter,name='filter'),
    path('review/<str:myid>',views.review,name='review'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    path("handlerequest1/", views.handlerequest1, name="HandleRequest1"),


]