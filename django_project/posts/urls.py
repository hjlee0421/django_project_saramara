from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('test/', views.TestIndexView.as_view(), name='testindex'),
    path('testask/', views.TestAskView.as_view(), name='testask'),
    path('accounts/login/kakao', views.kakao_login, name='kakaologin'),
    path('accounts/login/kakao/callback',
         views.kakao_callback, name='kakaocallback'),

]
