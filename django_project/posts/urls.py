from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/add_comment/', views.DetailView.as_view(), name="add_comment"),
    # path('<int:pk>/add_comment/', views.add_comment, name="add_comment"),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    path('test/', views.TestIndexView.as_view(), name='testindex'),
    path('testask/', views.TestAskView.as_view(), name='testask'),
    # url(r'^table/$',views.table),
    # url(r'^search/$', views.search_table, name="search_table"),
    path('kakao_login/', views.kakao_login_home, name="kakao_login_home"),
    path('<int:pk>/kakao_login/', views.kakao_login, name="kakao_login"),
    path('kakao_logout/', views.kakao_logout_home, name="kakao_logout_home"),
    path('<int:pk>/kakao_logout/', views.kakao_logout, name="kakao_logout"),
    # url(r'^<int:pk>/search/$', views.search_table, name="search_table"),
    path('<int:pk>/search/', views.kakao_login, name="kakao_login"),
    # 왜 이거는 안될까?
]
# path('accounts/login/kakao', views.kakao_login, name='kakaologin'),
# path('accounts/login/kakao/callback',
#      views.kakao_callback, name='kakaocallback'),
# path('', views.Unread, name='Unread'),
# url(r'^$', views.my_def_in_view, name='my_def_in_view'),
# url(r'^$', views.YourViewsHere),
# path('accounts/logout/kakao', views.kakao_logout, name='kakaologout'),
# path('accounts/unlink/kakao', views.kakao_unlink, name='kakaounlink'),
