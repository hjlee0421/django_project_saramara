from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),
    path('<int:pk>/add_comment/', views.DetailView.as_view(), name="add_comment"),
    path('<int:pk>/sara/', views.DetailView.as_view(), name="sara_button"),
    path('<int:pk>/mara/', views.DetailView.as_view(), name="mara_button"),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('kakao_login/', views.kakao_login, name="kakao_login"),
    path('kakao_logout/', views.kakao_logout, name="kakao_logout"),
    path('kakao_unlink/', views.kakao_unlink, name='kakao_unlink'),
    path('user_info/', views.user_info, name='user_info'),
    path('UploadImage/', views.UploadImage, name='UploadImage'),
    # path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    # path('test/', views.TestIndexView.as_view(), name='testindex'),
    # path('testask/', views.TestAskView.as_view(), name='testask'),
]
