from django.urls import path
from . import views

app_name = 'susers'

urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    # path('signin/', views.signin, name='signin'),
    # path('signout/', views.signout, name='signout'),
    path('signout/', views.SignoutView.as_view(), name='signout'),
    # TODO: signout 도 class 형태로 바꿀수있나?
]
