from django.shortcuts import render
import os
from .models import Post, User, Comment, ViewCount
from .forms import PostForm
from django.views import generic, View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.core.paginator import Paginator

from datetime import datetime, timedelta

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer, AskSerializer

import urllib
import requests
import json
from django.http import JsonResponse

# There is Q objects that allow to complex lookups. Example:
# Item.objects.filter(Q(creator=owner) | Q(moderated=False))
from django.db.models import Q

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, 'secrets.json'), 'rb') as secret_file:
    secrets = json.load(secret_file)

# class IndexView(generic.ListView):
#    def get_queryset(self):
# TODO : IndeView를 활용해서 전체 리스트 볼때 1) 필터를 걸수있게 하고 2) pagination도 적용하기
# https://wayhome25.github.io/django/2017/05/02/CBV/
# https://stackoverflow.com/questions/52510586/how-to-filter-a-generic-listview


def add_comment(request, pk):
    comment_input = request.GET['comment_input']
    print(comment_input)
    return render(request, 'posts/detail.html')


def kakao_logout_home(request):
    if request.session.get('user_id'):
        del(request.session['user_id'])
    logout(request)
    # logout(request, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


def kakao_logout(request, pk):
    if request.session.get('user_id'):
        del(request.session['user_id'])
    logout(request)
    # logout(request, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


def kakao_login_home(request):
    LOGIN_INFO = json.loads(request.GET['LOGIN_INFO'])
    USER_INFO = json.loads(request.GET['USER_INFO'])

    # LOGIN_INFO = json.loads(request.POST['LOGIN_INFO'])
    # USER_INFO = json.loads(request.POST['USER_INFO'])
    # print(USER_INFO)
    access_token = LOGIN_INFO["access_token"]
    profile_json = USER_INFO
    username = str(profile_json['id'])+'@kakao'

    gender = ""
    email = ""
    birthday = ""

    if profile_json['kakao_account']['gender_needs_agreement'] == False:
        gender = profile_json['kakao_account']['gender']

    if profile_json['kakao_account']['email_needs_agreement'] == False:
        email = profile_json['kakao_account']['email']

    if profile_json['kakao_account']['birthday_needs_agreement'] == False:
        birthday = profile_json['kakao_account']['birthday']

    if not User.objects.filter(username=username).exists():
        # 기존에 username 이 없다면
        user = User(username=username, gender=gender, email=email,
                    birthday=birthday, kakao_access_token=access_token)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return render(request, 'posts/ask.html')
        # return redirect('/')
    else:
        # 기존에 username 이 있다면?
        print("#######################")
        user = User.objects.get(username=username)
        # user = authenticate(username=username)
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return render(request, 'posts/ask.html')
        # return redirect('/')

    # return redirect('/')
    return render(request, 'posts/ask.html')


def kakao_login(request, pk):
    LOGIN_INFO = json.loads(request.GET['LOGIN_INFO'])
    USER_INFO = json.loads(request.GET['USER_INFO'])

    access_token = LOGIN_INFO["access_token"]
    profile_json = USER_INFO
    username = str(profile_json['id'])+'@kakao'

    gender = ""
    email = ""
    birthday = ""

    if profile_json['kakao_account']['gender_needs_agreement'] == False:
        gender = profile_json['kakao_account']['gender']

    if profile_json['kakao_account']['email_needs_agreement'] == False:
        email = profile_json['kakao_account']['email']

    if profile_json['kakao_account']['birthday_needs_agreement'] == False:
        birthday = profile_json['kakao_account']['birthday']

    if not User.objects.filter(username=username).exists():
        # 기존에 username 이 없다면
        user = User(username=username, gender=gender, email=email,
                    birthday=birthday, kakao_access_token=access_token)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return render(request, 'posts/ask.html')
        # return redirect('/')
    else:
        # 기존에 username 이 있다면?
        print("#######################")
        user = User.objects.get(username=username)
        # user = authenticate(username=username)
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return render(request, 'posts/ask.html')
        # return redirect('/')

    # return redirect('/')
    return render(request, 'posts/ask.html')


class IndexView(generic.ListView):

    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_objects'

    paginate_by = 10

    # def get_queryset(self):
    # return Post.objects.all()

    # 조회수순, 사라순, 마라순, 오늘, 이번주, 이번달.
    # order_by는 마지막에 해줘야 함

    def get(self, request, *args, **kwargs):
        # if request.method == 'GET':
        timerange = request.GET.get('timerange')
        timerange_list = ['1일', '7일', '30일']

        drone = request.GET.get('drone')
        drone_list = ['view_cnt', 'comment_cnt', 'sara_cnt', 'mara_cnt']

        category = request.GET.get('category')
        category_list = ['상의', '하의', '신발', '기타']

        keyword = request.GET.get('keyword')

        if timerange in timerange_list:
            self.queryset = self.get_queryset().filter(
                pub_date__gte=datetime.now()-timedelta(days=int(timerange[:-1])))

        if category in category_list:
            self.queryset = self.get_queryset().filter(category=category)

        if keyword:
            self.queryset = self.get_queryset().filter(Q(title__icontains=keyword)
                                                       | Q(ckcontent__icontains=keyword))
            # TODO : filter 여러가지 기능 추가하기
            # https://docs.djangoproject.com/en/3.1/ref/models/querysets/

        if drone in drone_list:
            self.queryset = self.get_queryset().order_by('-'+drone)

        # 부모클래스의 get 함수를 대신호출하는 방법
        return super(IndexView, self).get(request, *args, **kwargs)
#              <- ListView와 같음  ->

    # def listing(request):
    #     # post_objects = Post.objects.all()
    #     post_objects = Post.objects.filter(title__icontains='테스트')
    #     print(post_objects)
    #     paginator = Paginator(post_objects, 10)  # Show 10 contacts per page.

    #     page_number = request.GET.get('page')
    #     page_obj = paginator.get_page(page_number)
    #     return render(request, 'posts/index.html.html', {'page_obj': page_obj})


class DetailView(generic.DetailView, View):

    # NEED model & form_class
    model = Post
    form_class = PostForm

    def get(self, request, pk, *args, **kwargs):
        # if request.method == 'GET':

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comment'] = self.object.comment_set.all()

        if len(request.GET):
            comment_input = request.GET["comment_input"]
            print(comment_input)
            user = request.user
            print(user)
            # user = 현재 로그인한 username
            self.add_comment(user, comment_input)

        self.object.view_cnt = self.object.view_cnt + 1
        self.object.save()

        return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

        # TODO : 현재는 해당 페이지가 GET 요청할때마다 1씩 올라감, 하지만 하루에 한번으로 업데이트 해야함
        # print("###############################################")
        # print(request.session)
        # print(type(request.session))
        # print(request.session.get('user_id'))
        # print(type(User.objects.get(pk=request.session.get('user_id'))))
        # try:
        #     # ip주소와 게시글 번호로 기록을 조회함
        #     views = ViewCount.objects.get(
        #         user=User.objects.get(pk=request.session.get('user_id')), post=self.object)

        # except Exception as e:
        #     # 처음 게시글을 조회한 경우엔 조회 기록이 없음
        #     print(e)
        #     views = ViewCount(user=User.objects.get(
        #         pk=request.session.get('user_id')), post=self.object)
        #     self.object.view_cnt = self.object.view_cnt + 1
        #     views.view_cnt = views.view_cnt + 1
        #     views.save()
        # else:
        #     # 조회 기록은 있으나, 날짜가 다른 경우
        #     if not hits.date == timezone.now().date():

        #         self.object.view_cnt = self.object.view_cnt + 1
        #         views.view_cnt = views.view_cnt + 1
        #         views.date = timezone.now()
        #         views.save()
        #     # 날짜가 같은 경우
        #     else:
        #         print(str(ip) + ' has already hit this post.\n\n')

    def post(self, request, pk, *args, **kwargs):
        # if request.method == 'POST':

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comment'] = self.object.comment_set.all()

        user = request.user
        # user = 현재 로그인한 username

        if 'delete_comment_button' in request.POST:
            comment_id = request.POST['delete_comment']
            comment = Comment.objects.get(id=comment_id)
            if user == comment.author:
                comment.delete()
                self.object.comment_cnt = Comment.objects.filter(
                    post=Post.objects.filter(title=self.object).values('id')[0]['id']).count()
                self.object.save()
        if 'sara_button' in request.POST:
            self.sara_vote(user)
        elif 'mara_button' in request.POST:
            self.mara_vote(user)
        elif 'add_comment' in request.POST:
            self.add_comment(user, request.POST.get('add_comment'))

        return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def add_comment(self, user_name, user_comment):

        post = self.object

        comment = Comment(post=post, author=user_name, text=user_comment)
        comment.save()

        post.comment_cnt = post.comment_cnt = Comment.objects.filter(
            post=Post.objects.filter(title=post).values('id')[0]['id']).count()
        post.save()

    def sara_vote(self, user_name):
        post = self.object
        user_name = user_name.username

        sara_str = post.sara
        mara_str = post.mara

        if sara_str is None:
            sara_list = []
        else:
            sara_list = sara_str.split(' ')

        if mara_str is None:
            mara_list = []
        else:
            mara_list = mara_str.split(' ')

        if user_name in sara_list:
            sara_list.remove(user_name)

        elif user_name in mara_list:
            mara_list.remove(user_name)
            sara_list.append(user_name)

        else:
            sara_list.append(user_name)

        if '' in sara_list:
            sara_list.remove('')
        if '' in mara_list:
            mara_list.remove('')

        post.sara_cnt = len(sara_list)
        post.mara_cnt = len(mara_list)

        sara_str = ' '.join(sara_list)
        mara_str = ' '.join(mara_list)

        post.sara = sara_str
        post.mara = mara_str

        post.save()

    def mara_vote(self, user_name):
        post = self.object
        user_name = user_name.username

        mara_str = post.mara
        sara_str = post.sara

        if mara_str is None:
            mara_list = []
        else:
            mara_list = mara_str.split(' ')

        if sara_str is None:
            sara_list = []
        else:
            sara_list = sara_str.split(' ')

        if user_name in mara_list:
            mara_list.remove(user_name)
        elif user_name in sara_list:
            sara_list.remove(user_name)
            mara_list.append(user_name)
        else:
            mara_list.append(user_name)

        if '' in mara_list:
            mara_list.remove('')
        if '' in sara_list:
            sara_list.remove('')

        post.mara_cnt = len(mara_list)
        post.sara_cnt = len(sara_list)

        mara_str = ' '.join(mara_list)
        sara_str = ' '.join(sara_list)

        post.mara = mara_str
        post.sara = sara_str

        post.save()


class AskView(View):
    def get(self, request):
        # if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts/ask.html', {'form': form})
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def post(self, request):
        # if request.method == 'POST':

        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            post = Post(**form.cleaned_data)
            post.author = user
            post.save()
            return redirect('/')
        else:
            return render(request, 'posts/ask.html', {'form': form})
            # render(request, template_name, context=None, content_type=None, status=None, using=None)


class SignupView(View):
    def get(self, request):
        # if request.method == 'GET':
        return render(request, 'posts/signup.html')
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def post(self, request):
        # if request.method == 'POST':

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        res_data = {}

        if not(username and password and re_password):
            res_data['error'] = "모든값을 입려해주세요."
        elif password != re_password:
            res_data['error'] = "비밀번호가 다릅니다."
        else:
            # 여기가 결국 회원가입 포인트
            user = User.objects.create_user(
                username, email=None, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            request.session['user_id'] = user.id
            return redirect('/')

        return render(request, 'posts/signup.html', res_data)


class SigninView(View):
    def get(self, request):
        # if request.method == 'GET':
        return render(request, 'posts/signin.html')

    def post(self, request):
        # if request.method == 'POST':

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}

        if not(username and password):
            res_data['error'] = "모든값을 입려해주세요."
        elif not(authenticate(username=username, password=password)):
            res_data['error'] = "모든값을 입려해주세요."
        else:
            # 여기가 결국 로그인 포인트
            user = authenticate(username=username, password=password)
            login(request, user)
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return redirect('/')
            else:
                res_data['error'] = "비밀번호가 틀렸습니다."
        return render(request, 'posts/signin.html', res_data)


class SignoutView(View):
    def get(self, request):
        # if request.method == 'GET':
        if request.session.get('user_id'):
            access_token = User.objects.get(pk=request.session.get(
                'user_id')).kakao_access_token
            profile_request = requests.post(
                "https://kapi.kakao.com/v1/user/logout",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            del(request.session['user_id'])

        logout(request)
        # logout(request, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')


class MypageView(View):
    def get(self, request):
        # if request.method == 'GET':
        return render(request, 'posts/mypage.html')


# def Unread(request):
#     print(request.POST)
#     count = request.POST.get(['count'])

#     print("hello")

#     print("count status ", count)


# def my_def_in_view(request):
#     result = request.GET.get('result')
#     print(type(result))
#     result = request.POST.get('result')
#     print(type(result))

#     # Any process that you want
#     data = {
#         "apple": "please",
#     }
#     return JsonResponse(data)


# def YourViewsHere(request):
#     # if request.method == 'GET':
#     #     pass
#     #     # do_something()
#     if request.method == 'POST':
#         # access you data by playing around with the request.POST object
#         request.POST.get('data')
#         print(request.POST.get('data'))


# 회원탈퇴 해당 아이디에 대해서 access token 을 계속 추적가능해야 함


# def kakao_unlink(request):

#     access_token = User.objects.get(
#         pk=request.session.get('user_id')).kakao_access_token
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v1/user/unlink", headers={"Authorization": f"Bearer {access_token}"},)
#     # profile_json = profile_request.json()
#     # return HttpResponse(f'{profile_json}')
#     return redirect('/')
# # 로그아웃 해당 아이디에 대해서 access token 을 계속 추적가능해야 함


# def kakao_logout(request):
#     #     if request.method == 'GET':
#     #         if request.session.get('user_id'):
#     #             print(request.session.get('user_id'))
#     #             # access_token = User.object.filter()
#     #             profile_request = requests.post(
#     # "https://kapi.kakao.com/v1/user/logout",
#     #         headers={"Authorization": f"Bearer {access_token}"},
#     #     )
#     #             del(request.session['user_id'])

#     #         logout(request, backend='django.contrib.auth.backends.ModelBackend')

#     #         return redirect('/')

#     access_token = 'YqY4ghTnrJglEySNp44at2oXv9wSQZ5NITh_yAopb1QAAAF2E1hnFQ'
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v1/user/logout",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()
#     return HttpResponse(f'{profile_json}')


# class SignoutView(View):
#     def get(self, request):
#         # if request.method == 'GET':
#         if request.session.get('user_id'):
#             del(request.session['user_id'])
#         logout(request)

#         # return redirect('/')


# # # 처음이라면 회원가입, 아니라면 로그인
# def kakao_login(request):
#     # app_rest_api_key = os.getenv("APP_REST_API_KEY") TsecretsODO : os.getenv 방법도 정리해 둘것
#     javascript_key = ["kakao"]["javascript_key"]
#     redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"
#     return redirect(
#         f"https://kauth.kakao.com/oauth/authorize?client_id={javascript_key}&redirect_uri={redirect_uri}&response_type=code"
#     )


# def kakao_callback(request):

#     user_token = request.GET.get("code")

#     # app_rest_api_key = os.getenv("APP_REST_API_KEY")
#     javascript_key = secrets["kakao"]["javascript_key"]
#     url = 'https://kauth.kakao.com/oauth/token'
#     redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"

#     token_request = requests.post(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={javascript_key}&redirect_uri={redirect_uri}&code={user_token}"
#     )

#     token_response_json = token_request.json()
#     error = token_response_json.get("error", None)

#     # if there is an error from token_request
#     if error is not None:
#         raise KakaoException()
#     access_token = token_response_json.get("access_token")
#     print(access_token)
#     # post request
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()
#     print(profile_json)
#     username = str(profile_json['id'])+'@kakao'

#     gender = ""
#     email = ""
#     birthday = ""

#     if profile_json['kakao_account']['gender_needs_agreement'] == False:
#         gender = profile_json['kakao_account']['gender']

#     if profile_json['kakao_account']['email_needs_agreement'] == False:
#         email = profile_json['kakao_account']['email']

#     if profile_json['kakao_account']['birthday_needs_agreement'] == False:
#         birthday = profile_json['kakao_account']['birthday']

#     if not User.objects.filter(username=username).exists():
#         # 기존에 username 이 없다면
#         user = User(username=username, gender=gender, email=email,
#                     birthday=birthday, kakao_access_token=access_token)
#         user.save()
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         request.session['user_id'] = user.id
#         return redirect('/')
#     else:
#         # 기존에 username 이 있다면?
#         print("#######################")
#         user = User.objects.get(username=username)
#         # user = authenticate(username=username)
#         print(user)
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         request.session['user_id'] = user.id
#         return redirect('/')

#     # return HttpResponse(f'{profile_json}')
#     return redirect('/')

# ##############################################################################################################################
# # add new


class TestIndexView(generics.ListAPIView):  # CreateAPIView
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TestAskView(APIView):
    serializer_class = AskSerializer

    def post(self, request, format=None):
        # if request.method == 'POST':

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            # TODO : change to post = Post(**form.cleaned_data) style
            author = User.objects.get(pk=serializer.data.get('author'))
            title = serializer.data.get('title')
            price = serializer.data.get('price')
            brand = serializer.data.get('brand')
            link = serializer.data.get('link')
            ckcontent = serializer.data.get('ckcontent')
            category = serializer.data.get('category')

            post = Post(author=author, title=title, price=price, brand=brand,
                        link=link, ckcontent=ckcontent, category=category)
            post.save()
            return Response(AskSerializer(post).data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

##############################################################################################################################
