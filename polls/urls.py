from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hungry/', views.hungry, name='hungry'),
    path('out-or-in/', views.out_or_in, name='out_or_in'),
    path('orderer/', views.orderer, name='orderer'),
    path('food-choice/', views.food_choice, name='food_choice'),
    path('order-menu/', views.order_menu, name='order_menu'),
    path('review/', views.review, name='review'),
    path('clear/', views.clear, name='clear')
]
