from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'posts'

# view.함수명 인 url들 모두 class based view 로 변경한 후 views.클래스명.as_view() 로 변경하기
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),  # 메인 인데스
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),  # 포스트 디테일
    path('<int:pk>/edit/', views.EditView.as_view(), name='edit'),  # 포스트 디테일 > 편집
    path('mypage/', views.MypageView.as_view(), name='mypage'),  # 마이페이지
    path('ask/', views.AskView.as_view(), name='ask'),  # 질문하기
    # 프로필이미지 & 닉네임 변경 url 주소 이해하기 쉽게 변경작업 해야함
    path('upload_image/', views.upload_image, name="upload_image"),
    # 프로필 변경할때 사진부분 서버로 넘기는 작업처리
    path('add_image/', views.addImage_view, name="add_image"),
    # 프로필 변경할때 사진부분 클라이언트로 가져오는 작업처리
    path('get_images/', views.getImages_view, name="get_images"),
    path('kakao_login/', views.KakaoLoginView.as_view(),
         name="kakao_login"),  # 카카오 로그인
    path('kakao_logout/', views.KakaoLogoutView.as_view(),
         name="kakao_logout"),  # 카카오 로그아웃
    path('kakao_unlink/', views.KakaoUnlinkView.as_view(),
         name='kakao_unlink'),  # 카카오 연동해제
]
