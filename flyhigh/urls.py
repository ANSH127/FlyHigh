
from django.contrib import admin
from django.urls import path,include
from flyhigh import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mybooking/', views.mybooking, name='mybooking'),
    path('flights/', views.flights, name='flights'),
    path('filter/',views.filter,name='filter'),
    path('review/<str:myid>',views.review,name='review'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    path("handlerequest1/", views.handlerequest1, name="HandleRequest1"),
    path("create_pdf/", views.create_pdf, name="create_pdf"),
    path("check/", views.check, name="check"),
    path('signup/', views.handleSignup, name='signup'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.handleLogout, name='logout'),



]