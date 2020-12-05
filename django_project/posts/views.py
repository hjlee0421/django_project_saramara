import os
from .models import Post, User, Comment  # , HitCount

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.views import generic, View
from django.views.generic.edit import FormMixin

from .forms import PostForm

from django.core.paginator import Paginator

from datetime import datetime, timedelta

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer, AskSerializer

import urllib
import requests


# There is Q objects that allow to complex lookups. Example:
# Item.objects.filter(Q(creator=owner) | Q(moderated=False))
from django.db.models import Q

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, 'secrets'), 'rb') as secret_file:
    secrets = json.load(secret_file)

# class IndexView(generic.ListView):
#    def get_queryset(self):
# TODO : IndeView를 활용해서 전체 리스트 볼때 1) 필터를 걸수있게 하고 2) pagination도 적용하기
# https://wayhome25.github.io/django/2017/05/02/CBV/
# https://stackoverflow.com/questions/52510586/how-to-filter-a-generic-listview


# class DetailView(generic.DetailView, FormMixin, View):
#   def get(self, request, *args, **kwargs):
#   def post(self, request, *args, **kwargs):
#   def add_comment(self, user_name, user_comment):
#   def delete(self, request, *args, **kwargs):
#   def sara_vote(self, user_name):
#   def mara_vote(self, user_name):
# TODO :

# class AskView(View):
#   def get(self, request):
#   def post(self, request):
# TODO :

# class SignupView(View):
#   def get(self, request):
#   def post(self, request):
# TODO :

# class SigninView(View):
#   def get(self, request):
#   def post(self, request):
# TODO :

# class SignoutView(View):
#   def get(self, request):
# TODO :

# class MypageView(View):
#   def get(self, request):
# TODO :


# 회원탈퇴 해당 아이디에 대해서 access token 을 계속 추적가능해야 함


def kakao_unlink(request):

    access_token = User.objects.get(
        pk=request.session.get('user_id')).kakao_access_token
    profile_request = requests.post(
        "https://kapi.kakao.com/v1/user/unlink", headers={"Authorization": f"Bearer {access_token}"},)
    # profile_json = profile_request.json()
    # return HttpResponse(f'{profile_json}')
    return redirect('/')
# 로그아웃 해당 아이디에 대해서 access token 을 계속 추적가능해야 함


def my_view(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('result')


def kakao_logout(request):
    #     if request.method == 'GET':
    #         if request.session.get('user_id'):
    #             print(request.session.get('user_id'))
    #             # access_token = User.object.filter()
    #             profile_request = requests.post(
    # "https://kapi.kakao.com/v1/user/logout",
    #         headers={"Authorization": f"Bearer {access_token}"},
    #     )
    #             del(request.session['user_id'])

    #         logout(request, backend='django.contrib.auth.backends.ModelBackend')

    #         return redirect('/')

    access_token = 'YqY4ghTnrJglEySNp44at2oXv9wSQZ5NITh_yAopb1QAAAF2E1hnFQ'
    profile_request = requests.post(
        "https://kapi.kakao.com/v1/user/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    return HttpResponse(f'{profile_json}')


class SignoutView(View):
    def get(self, request):
        if request.session.get('user_id'):
            del(request.session['user_id'])

        logout(request)

        return redirect('/')


# 처음이라면 회원가입, 아니라면 로그인
def kakao_login(request):
    app_rest_api_key = os.getenv("APP_REST_API_KEY")
    redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):

    user_token = request.GET.get("code")

    app_rest_api_key = os.getenv("APP_REST_API_KEY")
    url = 'https://kauth.kakao.com/oauth/token'
    redirect_uri = "http://127.0.0.1:8000/accounts/login/kakao/callback"

    token_request = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={user_token}"
    )

    token_response_json = token_request.json()
    error = token_response_json.get("error", None)

    # if there is an error from token_request
    if error is not None:
        raise KakaoException()
    access_token = token_response_json.get("access_token")

    # post request
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    print(profile_json)
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
        return redirect('/')
    else:
        # 기존에 username 이 있다면?
        print("#######################")
        user = User.objects.get(username=username)
        # user = authenticate(username=username)
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        request.session['user_id'] = user.id
        return redirect('/')

    # return HttpResponse(f'{profile_json}')
    return redirect('/')

##############################################################################################################################
# add new


class TestIndexView(generics.ListAPIView):  # CreateAPIView
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class TestAskView(APIView):
    serializer_class = AskSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print("###############")
            print(serializer.data)

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


class IndexView(generic.ListView):

    print(secrets)

    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_objects'
    paginate_by = 10

    # def get_queryset(self):
    # return Post.objects.all()

    # 조회수순, 사라순, 마라순, 오늘, 이번주, 이번달.
    # order_by는 마지막에 해줘야 함

    def get(self, request, *args, **kwargs):

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

        '''
            $python manage.py shell_plus
            >>> Post.objects.all()
<QuerySet [<Post: 새로운 유저>, <Post: xptm>, <Post: 색깔별 모자>, <Post: 나이키를 살까 말까>, <Post: 어 이게 되나? 위 하의 아래 기타>, <Post: 하의라고>, <Post: 카테고리가 되나? 하의>, <Post: dho>, <Post: 클래스가>, <Post: 제목입니다>, <Post: 테스트유저1>, <Post: 테스트2>, <Post: 사진이 올라가기는 하는데>, <Post: 이게>, <Post: 이건 뭐지?>, <Post: 이제>, <Post: 체크하기>, <Post: 22>, <Post: 리치텍스트>, <Post: 11>, '...(remaining elements truncated)...']>
>>> Post.objects.all().count()
21
>>> Post.objects.filter(title__icontains='테스트')
<QuerySet [<Post: 테스트유저1>, <Post: 테스트2>]>
>>> Post.objects.filter(title__icontains='사진')
<QuerySet [<Post: 사진이 올라가기는 하는데>]>
>>> Post.objects.filter(title='테스트')
<QuerySet []>
>>> Post.objects.filter(title='테스트유저1')
<QuerySet [<Post: 테스트유저1>]>
>>> Post.objects.filter(title__icontains='테스트').values()
<QuerySet [{'id': 25, 'author_id': 3, 'title': '테스트유저1', 'price': '1만원', 'brand': '나이키', 'link': '없음', 'pup_date': datetime.datetime(2020, 11, 1, 6, 28, 22, 682023, tzinfo=<UTC>), 'sara': None, 'mara': None, 'sara_cnt': 0, 'mara_cnt': 0, 'ckcontent': '<p>여기는 ck content</p>', 'category': '상의'}, {'id': 24, 'author_id': 1, 'title': '테스트2', 'price': '스', 'brand': '테', 'link': '트', 'pup_date': datetime.datetime(2020, 10, 21, 11, 45, 25, 310006, tzinfo=<UTC>), 'sara': None, 'mara': None, 'sara_cnt': 0, 'mara_cnt': 0, 'ckcontent': '<p>테스트2</p>', 'category': '상의'}]>
>>> Post.objects.filter(title__icontains='테스트')
'''

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


class DetailView(generic.DetailView, FormMixin, View):
    model = Post
    form_class = PostForm
    template_name = 'posts/detail.html'

    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()

        self.object.view_cnt = self.object.view_cnt + 1
        self.object.save()
        # TODO : 현재는 해당 페이지가 GET 요청할때마다 1씩 올라감, 하지만 하루에 한번으로 업데이트 해야함

        context = self.get_context_data(object=self.object)
        context['comment'] = self.object.comment_set.all()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        user = request.user
        # post = Post(author=user, title='test for POST')

        if 'delete_comment_button' in request.POST:
            comment_id = request.POST['delete_comment']
            comment = Comment.objects.get(id=comment_id)
            if user == comment.author:
                comment.delete()

                self.object.comment_cnt = Comment.objects.filter(
                    post=Post.objects.filter(title=self.object).values('id')[0]['id']).count()
                self.object.save()

        context = self.get_context_data(object=self.object)

        if 'sara_button' in request.POST:
            self.sara_vote(user)
        elif 'mara_button' in request.POST:
            self.mara_vote(user)
        elif 'add_comment' in request.POST:
            self.add_comment(user, request.POST.get('add_comment'))
        context['comment'] = self.object.comment_set.all()
        return self.render_to_response(context)

    def add_comment(self, user_name, user_comment):
        post = self.object

        user_name = user_name
        comment = Comment(post=post, author=user_name, text=user_comment)
        comment.save()

        post.comment_cnt = post.comment_cnt = Comment.objects.filter(
            post=Post.objects.filter(title=post).values('id')[0]['id']).count()
        post.save()

    def delete(self, request, *args, **kwargs):

        return HttpResponse('context')

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
        form = PostForm()
        return render(request, 'posts/ask.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            post = Post(**form.cleaned_data)
            post.author = user
            post.save()
            return redirect('/')
        else:
            return redirect('/')


class SignupView(View):
    def get(self, request):
        return render(request, 'posts/signup.html')

    def post(self, request):
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
        return render(request, 'posts/signin.html')

    def post(self, request):
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
        if request.session.get('user_id'):
            # print(request.session.get('user_id'))
            # print(User.objects.get(pk=request.session.get('user_id')))
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
        return render(request, 'posts/mypage.html')


# views.py
# try:
#     # ip주소와 게시글 번호로 기록을 조회함
#     hits = HitCount.objects.get(ip=ip, post=post)
# except Exception as e:
#     # 처음 게시글을 조회한 경우엔 조회 기록이 없음
#     print(e)
#     hits = HitCount(ip=ip, post=post)
#     SummerNote.objects.filter(
#         attachment_ptr_id=post_id).update(hits=post.hits + 1)
#     hits.save()
# else:
#     # 조회 기록은 있으나, 날짜가 다른 경우
#     if not hits.date == timezone.now().date():
#         SummerNote.objects.filter(
#             attachment_ptr_id=post_id).update(hits=post.hits + 1)
#         hits.date = timezone.now()
#         hits.save()
#     # 날짜가 같은 경우
#     else:
#         print(str(ip) + ' has already hit this post.\n\n')
