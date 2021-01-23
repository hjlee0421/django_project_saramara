
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from .models import Post, User, Comment, ViewCount, Image
from .forms import PostForm, EditForm

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


# @csrf_exempt, def 에 사용

@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(View):
    def post(self, request):
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


@method_decorator(csrf_exempt, name='dispatch')
class KakaoLogoutView(View):
    def post(self, request):
        if request.session.get('user_id'):
            del(request.session['user_id'])
        logout(request)
        # logout(request, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')


@method_decorator(csrf_exempt, name='dispatch')
class KakaoUnlinkView(View):
    def post(self, request):
        user_id = request.session.get('user_id')

        if request.session.get('user_id'):
            del(request.session['user_id'])

        logout(request)
        user = User.objects.get(pk=user_id)
        user.delete()
        # logout(request, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')


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
        context['images'] = post.image_set.all()
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


# class AskView(View):
class AskView(FormView):

    form_class = PostForm
    template_name = 'ask.html'  # Replace with your template.
    success_url = "/"  # Replace with your URL or reverse().

    def get(self, request):
        # if request.method == 'GET':
        form = PostForm()
        return render(request, 'posts/ask.html', {'form': form})
        # render(request, template_name, context=None, content_type=None, status=None, using=None)

    def post(self, request):

        files = request.FILES.getlist('item_image')

        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('item_images')

        if form.is_valid():
            user_id = request.session.get('_auth_user_id')
            user = User.objects.get(pk=user_id)
            post = Post(**form.cleaned_data)
            post.author = user
            post.save()

            for image in request.FILES.getlist('item_image'):
                image_obj = Image()
                image_obj.post_id = post.id
                image_obj.item_image = image
                image_obj.save()

            return redirect('/'+str(post.pk))
        else:
            return render(request, 'posts/ask.html', {'form': form})
        # render(request, template_name, context=None, content_type=None, status=None, using=None)


class EditView(generic.DetailView, View):
    model = Post
    form_class = PostForm

    def get(self, request, pk, *args, **kwargs):
        print("#####################")
        print("editview GET function")
        print("#####################")
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
        print("#####################")
        print("editview POST function")
        print("#####################")
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


@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(View):
    def get(self, request):
        # if request.method == 'GET':

        if "username_input" in request.GET:
            new_username = request.GET["username_input"]

            if not User.objects.filter(username=new_username).exists():
                return JsonResponse(data={'created': True})
            elif User.objects.filter(username=new_username).exists():
                return JsonResponse(data={'created': False, 'len': '2'})

        return render(request, "posts/user_profile.html")

    def post(self, request):
        # if request.method == 'POST':

        user_id = request.session.get('_auth_user_id')
        user = User.objects.get(pk=user_id)

        print(request.FILES)
        if "profile_image" in request.FILES:
            user.profile_image = request.FILES["profile_image"]

        print(request.POST)
        if "username" in request.POST:
            new_username = request.POST["username"]

            if not User.objects.filter(username=new_username).exists():
                user.username = new_username

        user.save()

        return redirect('/')


#############################################################################################

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
