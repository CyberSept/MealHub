from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('review/', views.review, name='review'),
    path('clear/', views.clear, name='clear'),
    path('random/', views.random_orderer, name='random'),
]
