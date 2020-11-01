from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # TODO : 현재 /pk/ 로 넘어가서 detail 페이지를 보여주는 view 부분을 아래처럼 변경해야 POST방식으로 사용 가능
    # path('/', views.PostView.as_view(), name='post'), >> POST 방식으로 투표를 하려면 이렇게 변경 되야 함
    path('mypage/', views.mypage, name='mypage'),
    path('ask/', views.ask, name='ask'),
]
# resutls 필요없을듯
