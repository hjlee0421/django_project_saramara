from django.utils.decorators import method_decorator
from .forms import UserForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from .models import Post, User, Comment, ViewCount
from .forms import UserForm, PostForm, EditForm
from django.views import generic, View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.core.paginator import Paginator

from datetime import datetime, timedelta
from django.utils import timezone

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


@csrf_exempt
def kakao_unlink(request):
    user_id = request.session.get('user_id')

    if request.session.get('user_id'):
        del(request.session['user_id'])

    logout(request)
    user = User.objects.get(pk=user_id)
    user.delete()
    # logout(request, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


@csrf_exempt
def kakao_logout(request):
    if request.session.get('user_id'):
        del(request.session['user_id'])
    logout(request)
    # logout(request, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')


@csrf_exempt
def kakao_login(request):  # , pk
    LOGIN_INFO = json.loads(request.POST['LOGIN_INFO'])
    USER_INFO = json.loads(request.POST['USER_INFO'])

    access_token = LOGIN_INFO["access_token"]
    profile_json = USER_INFO
    username = str(profile_json['id'])+'@kakao'

    gender = ""
    email = ""
    birthday = ""
    print(profile_json['kakao_account'])
    if profile_json['kakao_account']['has_gender'] is True:
        gender = profile_json['kakao_account']['gender']

    if profile_json['kakao_account']['has_email'] is True:
        email = profile_json['kakao_account']['email']

    if profile_json['kakao_account']['has_birthday'] is True:
        birthday = profile_json['kakao_account']['birthday']

    if not User.objects.filter(kakao_unique_id=str(profile_json['id'])).exists():
        # 기존에 username 이 없다면

        user = User(username=username, gender=gender, email=email, password=profile_json['id'],
                    birthday=birthday, kakao_access_token=access_token, kakao_unique_id=profile_json['id'])
        user.is_staff = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return JsonResponse({'created': True})
        # return render(request, 'posts/ask.html')
        # return redirect('/')
    else:
        # 기존에 username 이 있다면?

        user = User.objects.get(kakao_unique_id=profile_json['id'])
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return JsonResponse(data={'created': False, 'len': '2'})

    return render(request, 'posts/ask.html')


class IndexView(generic.ListView):

    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_objects'

    paginate_by = 10

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


# @csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class DetailView(generic.DetailView, View):

    # NEED model & form_class
    model = Post
    form_class = PostForm

    def get(self, request, pk, *args, **kwargs):
        # if request.method == 'GET':
        #  self.object 는 post 로 변경하기

        post = self.get_object()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # print(post.comment_set.all())
        context['comment'] = post.comment_set.all()
        user = request.user

        # render(request, template_name, context=None, content_type=None, status=None, using=None)

        # # 나이 성별은 나중에 view 에서 작업을 해서 html 에서 보여주는 방법으로 해야 함
        if request.session.get('user_id'):
            try:
                # ip주소와 게시글 번호로 기록을 조회함
                # TODO: post.view_set.all() 방식으로 수정해야 함
                views = ViewCount.objects.get(
                    loggedin_user=User.objects.get(pk=request.session.get('user_id')), post=post)
            except Exception as e:
                # 처음 게시글을 조회한 경우엔 조회 기록이 없음
                # TODO: post.view_set.all() 방식으로 수정해야 함
                views = ViewCount(loggedin_user=User.objects.get(
                    pk=request.session.get('user_id')), post=post)
                post.view_cnt = post.view_cnt + 1
                post.save()
                views.view_cnt = views.view_cnt + 1
                views.save()
            else:
                # 조회 기록은 있으나, 날짜가 다른 경우
                if not views.date.date() == timezone.now().date():

                    post.view_cnt = post.view_cnt + 1
                    post.save()
                    views.view_cnt = views.view_cnt + 1
                    views.date = timezone.now().date()
                    views.save()

        return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)

    def post(self, request, pk, *args, **kwargs):
        # if request.method == 'POST':

        post = self.get_object()
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comment'] = post.comment_set.all()

        user = request.user
        # user = 현재 로그인한 username
        print("################")
        print(request.POST)

        if 'saramara_input' in request.POST:
            saramara_input = request.POST["saramara_input"]
            if saramara_input == "sara":
                post.sara_vote(user)
            elif saramara_input == "mara":
                post.mara_vote(user)

        if 'comment_input' in request.POST:
            comment_input = request.POST["comment_input"]
            self.add_comment(user, comment_input)

        if 'new_comment' in request.POST:
            new_comment = request.POST["new_comment"]
            comment_pk = request.POST["pk"]
            self.edit_comment(comment_pk, new_comment)

        if 'delete_comment_pk' in request.POST:
            comment_id = request.POST['delete_comment_pk']
            comment = Comment.objects.get(id=comment_id)
            if user == comment.author:
                comment.delete()
                # post.comment_cnt = post.comment_set.all().count()
                post.save()
                print("삭제완료")
            # return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)

        if 'delete_post' in request.POST:
            post_id = request.POST['delete_post']
            post = Post.objects.get(id=post_id)

            if user == post.author:
                post.delete()
                print("post deleted")
                return redirect('/')
                # return render(request, 'posts/index.html')

        if 'edit_post_button' in request.POST:
            post_id = request.POST['edit_post']
            return redirect('/'+post_id+'/edit')
            # return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)
            # post.comment_cnt = post.comment_set.all().count()
            # post.save()

        # delete comment도 ajax로 처리가능할듯
        # if 'sara_button' in request.POST:
        #     self.sara_vote(user)
        # elif 'mara_button' in request.POST:
        #     self.mara_vote(user)
        # elif 'add_comment' in request.POST:
        #     pass
        # 추후삭제
            # self.add_comment(user, request.POST.get('add_comment'))

        return render(request, 'posts/detail.html', context=context, content_type=None, status=None, using=None)
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def add_comment(self, user_name, user_comment):
        print("add_comment called")
        post = self.object
        comment = Comment(post=post, author=user_name, text=user_comment)
        comment.save()

        # post.comment_cnt = post.comment_set.all().count()
        post.save()

    def edit_comment(self, pk, user_comment):

        comment = Comment.objects.get(pk=pk)
        comment.text = user_comment
        comment.save()


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
            return redirect('/'+str(post.pk))
        else:
            return render(request, 'posts/ask.html', {'form': form})
            # render(request, template_name, context=None, content_type=None, status=None, using=None)


class EditView(generic.DetailView, View):
    model = Post
    form_class = PostForm

    def get(self, request, pk, *args, **kwargs):
        # if request.method == 'GET':
        # post = Post(**form.cleaned_data)
        post = self.get_object()
        form = PostForm(instance=post)
        # context = self.get_context_data(form=form)
        context = dict(form=form)
        # TODO: 확인하기
        # import pdb
        # pdb.set_trace()
        # TODO: 게시글 수정 화면 내용 채우기
        # form 안에 context? 로 내용을 채워야 할듯
        return render(request, 'posts/edit.html', context=context,
                      content_type=None, status=None, using=None)
        # return render(request, 'posts/ask.html', {'form': form})
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def post(self, request, pk, *args, **kwargs):
        # if request.method == 'POST':

        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            post = self.get_object()

            # post = Post(**form.cleaned_data)
            post.title = form.cleaned_data['title']
            post.category = form.cleaned_data['category']
            post.brand = form.cleaned_data['brand']
            post.price = form.cleaned_data['price']
            post.link = form.cleaned_data['link']
            post.ckcontent = form.cleaned_data['ckcontent']

            post.author = user
            post.save()
            return redirect('/'+str(post.pk))
        else:
            return render(request, 'posts/ask.html', {'form': form})
            # render(request, template_name, context=None, content_type=None, status=None, using=None)


class MypageView(View):
    # paginate_by = 2

    def get(self, request):
        # if request.method == 'GET':
        return render(request, 'posts/mypage.html')


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

# def listing(request):
#     # post_objects = Post.objects.all()
#     post_objects = Post.objects.filter(title__icontains='테스트')
#     print(post_objects)
#     paginator = Paginator(post_objects, 10)  # Show 10 contacts per page.

#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'posts/index.html.html', {'page_obj': page_obj})


# class SignupView(View):
#     def get(self, request):
#         # if request.method == 'GET':
#         return render(request, 'posts/signup.html')
#         # render(request, template_name, context=None, content_type=None, status=None, using=None)

#     def post(self, request):
#         # if request.method == 'POST':

#         username = request.POST.get('username', None)
#         password = request.POST.get('password', None)
#         re_password = request.POST.get('re-password', None)

#         res_data = {}

#         if not(username and password and re_password):
#             res_data['error'] = "모든값을 입려해주세요."
#         elif password != re_password:
#             res_data['error'] = "비밀번호가 다릅니다."
#         else:
#             # 여기가 결국 회원가입 포인트
#             user = User.objects.create_user(
#                 username, email=None, password=password)
#             login(request, user)
#             user = User.objects.get(username=username)
#             request.session['user_id'] = user.id
#             return redirect('/')

#         return render(request, 'posts/signup.html', res_data)


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


#############################################################################################


# 해당 html 을 보여주기 위해서
def upload_image(request):
    user_id = request.session.get('user_id')
    username = User.objects.get(pk=user_id)
    newForm = UserForm()
    context = {"form": newForm, }

    if "username_input" in request.GET:
        new_username = request.GET["username_input"]

        if not User.objects.filter(username=new_username).exists():
            user = User.objects.get(pk=user_id)
            user.username = new_username
            user.save()
            return JsonResponse({'created': True})
    return render(request, "posts/upload_image.html", context)


# @csrf_exempt
# def user_info(request):
#     user_id = request.session.get('user_id')
#     username = User.objects.get(pk=user_id)

#     newForm = UserForm()
#     context = {"form": newForm, }
#     # return render(request, "posts/upload_image.html", context)

#     if "username_input" in request.GET:
#         new_username = request.GET["username_input"]

#         if not User.objects.filter(username=new_username).exists():
#             user = User.objects.get(pk=user_id)
#             user.username = new_username
#             user.save()
#             return JsonResponse({'created': True})

#     return render(request, 'posts/user_info.html', context)
#     # return render(request, 'posts/user_info.html', context)


# submit 버튼을 눌렀을때 저장하기 위해서


# def addImage_view(request):
#     form = ImageForm(request.POST, request.FILES)
#     print("request.files")
#     print(request.FILES)
#     print("request.files type")
#     print(type(request.FILES))
#     user = User.objects.first()
#     user.profile_image = request.FILES["profile_image"]
#     user.save()
#     if(form.is_valid()):
#         form.save()
#         print("form saved")
#     return HttpResponse("success")

# 저장된 이미지를 보기 위해서


def getImages_view(request):
    # images = User.objects.all()
    user_id = request.session.get('_auth_user_id')
    user = User.objects.get(pk=user_id)
    image_urls = []
    print(str(user.profile_image))
    image_urls.append("media/"+str(user.profile_image))
    response = {"image_urls": "/media/"+str(user.profile_image)}
    return JsonResponse(response)


# @csrf_exempt
# def UploadImage(request):
#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#         pass
#     return JsonResponse(data={'created': False, 'len': '2'})
#     # pic = request.FILES['image']  # I don't know if this is correct

@csrf_exempt
def addImage_view(request):
    form = UserForm(request.POST, request.FILES)
    print("request.files")
    print(request.FILES)
    print("request.files type")
    print(type(request.FILES))
    if(form.is_valid()):
        print('form is valid')
        user_id = request.session.get('_auth_user_id')
        user = User.objects.get(pk=user_id)
        user.profile_image = request.FILES["profile_image"]
        user.save()
    return HttpResponse("success")
    # return render(request, 'home.html', {'form': form, 'up': User.objects.get(pk=user_id), })


# @csrf_exempt
# def user_info(request):
#     user_id = request.session.get('user_id')
#     username = User.objects.get(pk=user_id)

#     newForm = UserForm()
#     context = {"form": newForm, }
#     # return render(request, "posts/upload_image.html", context)

#     if "username_input" in request.GET:
#         new_username = request.GET["username_input"]

#         if not User.objects.filter(username=new_username).exists():
#             user = User.objects.get(pk=user_id)
#             user.username = new_username
#             user.save()
#             return JsonResponse({'created': True})

#     return render(request, 'posts/user_info.html', context)
#     # return render(request, 'posts/user_info.html', context)

#     '''
#     POST 로 값을 전달받아서,(x)
#     ajax로 값을 전달 받아서 아래 내용을 확인하고
#     if User.objects.filter(username=username).exists():
#         raise forms.ValidationError('아이디가 이미 사용중입니다')
#         username 이 존재함을 return
#     else
#         username 이 사용가능함을 return
#     '''

#     '''
#     profile 이미지의 경우 ajax로 처리해야 업로드 후 이미지 바로 표현
#     사진을 업로드 하면 이미지 사이즈를 resize 해서,
#     해당 html 에서 바로 올린 이미지가 보이게끔 처리
#     '''

#     '''
#     마지막에 시작하기 버튼을 누르면 위 변경사항들을 모두 적용해서 save 후 redirect
#     user.username = 전달받은 값
#     '''
