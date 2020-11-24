from django.urls import path
from . import views

urlpatterns = [
    path('tt', views.index),
    path('join', views.index),
    path('create', views.index)
]
