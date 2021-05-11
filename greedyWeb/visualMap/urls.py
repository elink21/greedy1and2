from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('greedyA', views.greedyA, name='GreedyA'),
    path('greedyB', views.greedyB, name='GreedyB'),
]
