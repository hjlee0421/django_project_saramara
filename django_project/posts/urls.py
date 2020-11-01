from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('/', views.PostView.as_view(), name='post'),   >> post 방식으로 투표를 하려면 이렇게 변경되는쪽으로 TO-D0
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:post_id>/votes/', views.vote, name='vote'),
    path('mypage/', views.mypage, name='mypage'),
    path('ask/', views.ask, name='ask'),
]
# resutls 필요없을듯
