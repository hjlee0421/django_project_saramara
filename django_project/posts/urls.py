from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('mypage/', views.mypage, name='mypage'),
    # path('ask/', views.AskView.as_view(), name='ask'),
    path('ask/', views.ask, name='ask'),
]
