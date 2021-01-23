from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 메인 인데스
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # 포스트 디테일
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),  # 포스트 디테일 > 편집
    path('mypage/', views.MypageView.as_view(), name='mypage'),  # 마이페이지
    path('ask/', views.AskView.as_view(), name='ask'),  # 질문하기
    path('user_profile/', views.UserProfileView.as_view(),
         name="user_profile"),  # 유저정보
    path('kakao_login/', views.KakaoLoginView.as_view(),
         name="kakao_login"),  # 카카오 로그인
    path('kakao_logout/', views.KakaoLogoutView.as_view(),
         name="kakao_logout"),  # 카카오 로그아웃
    path('kakao_unlink/', views.KakaoUnlinkView.as_view(),
         name='kakao_unlink'),  # 카카오 연동해제
]
