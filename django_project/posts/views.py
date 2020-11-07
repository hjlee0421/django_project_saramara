from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Post  # , Choice
from django.urls import reverse
from django.views import generic, View
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from .forms import PostForm
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import User

# TODO : ??? MAIN PAGE 에서 카테고리별로 필터를 걸어주려면 아래의 ListView를 활용해서 보여줘야 함
# 현재는 IndexView 를 사용중임
# generic.ListView

# class IndexView(generic.ListView):
# TODO : IndeView를 활용해서 전체 리스트 볼때 1) 필터를 걸수있게 하고 2) pagination도 적용하기
# https://wayhome25.github.io/django/2017/05/02/CBV/
# https://stackoverflow.com/questions/52510586/how-to-filter-a-generic-listview
# class PostView(View):
#   def post(self, request, *args, **kwargs):
# TODO : PostView를 활용해서 아래의 DetailView를 대체해야 POST 방식으로 각각의 post 불러오고, update 가능함
# https://laziness.xyz/2017/05/Django-Class-based-view-post
# class DetailView(generic.DetailView, FormMixin):
#   def get(self, request, *args, **kwargs):
#   def sara_vote(self, user_name):
#   def mara_vote(self, user_name):
# def mypage(request):
# @ login_required
# def ask(request):
# TODO : def로 되어있는 부분을 class 형태로 변경하기


class IndexView(generic.ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'
    # paginate_by = 10

    def get_queryset(self):
        return Post.objects.all()  # .order_by('-id')


# https://docs.djangoproject.com/en/3.1/topics/class-based-views/intro/

# TODO : 아래의 PostView를 <int:pk> url 로 연결해서 각 Post model의 object 정보를 get 함수로 보여줄수있어야 함
# TODO : POST  방법을 이용해서 투표해도, 새로운 page가 계속 생기고 뒤로가기 할때 계속 화면이 보임 >> 아마 DRF 사용?
class PostView(SingleObjectMixin, View):  # generic.DetailView, FormMixin
    # class PostView(generic.detail.BaseDetailView, FormMixin):
    model = Post
    form_class = PostForm

    initial = {'key': 'value'}
    template_name = 'posts/detail.html'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class(initial=self.initial)
    #     return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        print('#########################################33')
        print('#########################################33')
        print('#########################################33')
        print('#########################################33')
        print('Hello, PostView get def')
        form = self.form_class(initial=self.initial)
        # print(form)
        # return render(request, self.template_name, {'form': form})
        # self.object = self.get_object()
        # context = self.get_context_data(object=self.object)
        # return self.render_to_response(context)
        return render(request, self.template_name, {'form': form})

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)  # , form=PostForm)
    #     context['comment'] = self.object.comment_set.all()
    #     return self.render_to_response(context)
        # print('Hello, PostView get def')
        # form = self.form_class(initial=self.initial)
        # return render(request, self.template_name, {'form': form})
        # context = {'Hello, PostView get def'}
        # return HttpResponse(context)
        # return HttpResponse('Hello, World!333')

    # get 없애고 post만 남으면 페이지 없으로 뜸

    def post(self, request, *args, **kwargs):
        print('#########################################33')
        print('#########################################33')
        print('#########################################33')
        print('#########################################33')
        print('Hello, PostView post def')
        user_id = request.session.get('_auth_user_id')
        suser = User.objects.get(pk=user_id)
        print('user : ', suser)
        print('please true, ', 'sara_button' in request.POST)
        print('please false, ', 'mara_button' in request.POST)

        print(request.POST)

        post = Post(author=suser, title='test for POST')

        if 'sara_button' in request.POST:
            sara_vote(post, suser)
        elif 'mara_button' in request.POST:
            mara_vote(post, suser)

        # # post.save()
        form = PostForm(request.POST)
        # if form.is_valid():
        #     print('Hello, PostView get def and form is valid')
        #     # process form cleaned data
        #     return HttpResponseRedirect('/test/')

        return render(request, self.template_name, {'form': form})
        # context = {'Hello, PostView post def'}
        # import pdb
        # pdb.set_trace()
        # return HttpResponse(context)
        # return HttpResponse(context)

    # post def 안에서 pdb 활용해서 뜯어보기
    # base.py 에서 view class 를 바로 post 함수를 override 하게 되는 class
    # list view 와 비슷하게
    # url이 먼저 잘 연결되는지 확인하고 안에 채우기


class DetailView(generic.DetailView, FormMixin):
    model = Post
    form_class = PostForm
    template_name = 'posts/detail.html'

    # get 이라는 함수는 html call 이랑 연관이 있고, 여기에 코드를 추가해줌으로 url을 get 할때 정보를 관리한다?
    # TODO : 추후에는 POST 방식으로 데이터를 변경을 한다.
    # DETAIL VIEW VS LIST VIEW
    # 게시글의 ID가 필요한게 DETAIL VIEW,  LIST VIEW 는 그러한 ID가 필요하지 않다.
    # 명확한 게시글을 고르는 경우 DETAIL VIEW, 아닌 경우는 LIST VIEW

    # https://stackoverflow.com/questions/36950416/when-to-use-get-get-queryset-get-context-data-in-django
    # https://stackoverflow.com/questions/16668441/django-get-and-post-handling-methods
    # https://docs.djangoproject.com/en/3.1/topics/class-based-views/mixins/
    # a better solution 부분

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     print('???')
    #     return HttpResponse('This is POST request')

    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        print(type(self.object))
        print(self.object.__dict__.keys())
        # print(self.object.content)

        # TODO : 여기에 그냥 form=PostForm 을 넣어주는게 맞는건가???
        # django - views - generic - base.py 에서 ContextMixin: 아래에
        # extra_context = None 으로 초기화해줘서 된건지 base.py 어딘가 다른곳에 초기화를 해준건지 확실하지 않음
        # 아마 맞는것 같음
        # class ContextMixin:
        """
        A default context mixin that passes the keyword arguments received by
        get_context_data() as the template context.
        """
        # extra_context = None
        # import pdb
        # pdb.set_trace()
        context = self.get_context_data(object=self.object)  # , form=PostForm)

        print('?')
        # print(context)
        # import pdb
        # pdb.set_trace()
        if len(request.get_full_path().split('?')) == 1:
            print('sara str')
            print(self.object.sara)
            print(self.object.sara_cnt)
            print('mara str')
            print(self.object.mara)
            print(self.object.mara_cnt)
            pass
        elif len(request.get_full_path().split('?')) == 2:
            if request.get_full_path().split('?')[1].split('=')[0] == 'sara':
                print("sara clicked")
                user_name = request.get_full_path().split('?')[1].split('=')[1]
                self.sara_vote(user_name)
            elif request.get_full_path().split('?')[1].split('=')[0] == 'mara':
                print("mara clicked")
                user_name = request.get_full_path().split('?')[1].split('=')[1]
                self.mara_vote(user_name)
        # import pdb
        # pdb.set_trace()
        context['comment'] = self.object.comment_set.all()
        return self.render_to_response(context)  # context
        # return HttpResponseRedirect(reverse('posts:detail', args=(self.object.id,)))

        # post.save()
        # 위 방식을 통해서 db에 저장
        # request의 url 을 통해서 확인하고 post 통해서 db update

    def add_comment(self, user_name):
        post = self.object
        user_name = user_name

    def sara_vote(self, user_name):
        post = self.object
        user_name = user_name

        sara_str = post.sara
        print('sara str')
        print(sara_str)

        mara_str = post.mara
        print('mara str')
        print(mara_str)

        if sara_str is None:
            sara_list = []
        else:
            sara_list = sara_str.split(' ')

        if mara_str is None:
            mara_list = []
        else:
            mara_list = mara_str.split(' ')

        print('sara list before')
        print(sara_list)

        print('mara list before')
        print(mara_list)

        if user_name in sara_list:
            print("1번 콜")
            # user_id in sara_str which means unvote for sara
            sara_list.remove(user_name)

        elif user_name in mara_list:
            print("2번 콜")
            # user_id in mara_list which means unvote for mara and vote for sara
            mara_list.remove(user_name)
            sara_list.append(user_name)

        else:
            print("3번 콜")
            # user_id not in both of sara or mara which means new
            sara_list.append(user_name)

        if '' in sara_list:
            sara_list.remove('')
        if '' in mara_list:
            mara_list.remove('')

        print('sara list after')
        print(sara_list)

        print('mara list after')
        print(mara_list)

        post.sara_cnt = len(sara_list)
        post.mara_cnt = len(mara_list)

        sara_str = ' '.join(sara_list)
        mara_str = ' '.join(mara_list)

        post.sara = sara_str
        post.mara = mara_str

        post.save()

    def mara_vote(self, user_name):

        post = self.object

        user_name = user_name

        mara_str = post.mara
        print('mara str')
        print(mara_str)

        sara_str = post.sara
        print('sara str')
        print(sara_str)

        if mara_str is None:
            mara_list = []
        else:
            mara_list = mara_str.split(' ')

        if sara_str is None:
            sara_list = []
        else:
            sara_list = sara_str.split(' ')

        if user_name in mara_list:
            # user_id in sara_str which means unvote for sara
            mara_list.remove(user_name)

        elif user_name in sara_list:
            # user_id in mara_list which means unvote for mara and vote for sara
            sara_list.remove(user_name)
            mara_list.append(user_name)

        else:
            # user_id not in both of sara or mara which means new
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


def mypage(request):
    return render(request, 'posts/mypage.html')


@ login_required
def ask(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        # import pdb
        # pdb.set_trace()
        if form.is_valid():
            # import pdb
            # pdb.set_trace()
            # user_id = request.session.get('user_id')
            user_id = request.session.get('_auth_user_id')
            print(user_id)
            suser = User.objects.get(pk=user_id)
            # post = Post()

            # post.title = form.cleaned_data['title']
            # post.brand = form.cleaned_data['brand']
            # post.price = form.cleaned_data['price']
            # post.link = form.cleaned_data['link']
            # post.content = form.cleaned_data['content']
            # post.ckcontent = form.cleaned_data['ckcontent']

            post = Post(**form.cleaned_data)
            # TODO : 위 코드를 통해서 추가가 되는 구조는 좋은 구조가 아니다, 위 코드 1줄로 다 해결가능 함

            post.author = suser
            post.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        form = PostForm()

    return render(request, 'posts/ask.html', {'form': form})

# class ResultsView(generic.DetailView):
#     model = Post
#     template_name = 'posts/results.html'


# action을 눌렀을때 무언가가 호출이 된다
# 링크를 누르면 어떤 함수가 호출이 된다


# copy and change sara <> mara
# ADD LOGIN STEP
# add @login_required
# def sara_vote(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)

#     user_id = request.session.get('user_id')

#     sara_str = post.sara
#     mara_str = post.mara

#     # check textfield is empty or not and create list
#     if not sara_str:
#         sara_list = sara_str.split(' ')
#     else:
#         sara_list = []

#     if not mara_str:
#         mara_list = mara_str.split(' ')
#     else:
#         mara_list = []

#     if str(user_id) in sara_list:
#         # user_id in sara_str which means unvote for sara
#         sara_list.remove(str(user_id))

#     elif str(user_id) in mara_list:
#         # user_id in mara_list which means unvote for mara and vote for sara
#         mara_list.remove(str(user_id))
#         sara_list.append(str(user_id))

#     else:
#         # user_id not in both of sara or mara which means new
#         sara_list.append(str(user_id))

#     sara_cnt = len(sara_list)
#     mara_cnt = len(mara_list)

#     sara_str = ' '.join(sara_list)
#     mara_str = ' '.join(mara_list)

#     Post.sara = sara_str
#     Post.mara = mara_str

#     # Always return an HttpResponseRedirect after successfully dealing
#     # with POST data. This prevents data from being posted twice if a
#     # user hits the Back button.
#     return HttpResponseRedirect(self.request.path_info)
    # return HttpResponseRedirect('<int:pk>', args=(post.id,))
    # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


# copy and change sara <> mara
# ADD LOGIN STEP
# add @login_required
# def mara_vote(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)

#     user_id = request.session.get('user_id')

#     mara_str = post.mara
#     sara_str = post.sara

#     # check textfield is empty or not and create list
#     if not mara_str:
#         mara_list = mara_str.split(' ')
#     else:
#         mara_list = []

#     if not sara_str:
#         sara_list = sara_str.split(' ')
#     else:
#         sara_list = []

#     if str(user_id) in mara_list:
#         # user_id in mara_str which means unvote for mara
#         mara_list.remove(str(user_id))

#     elif str(user_id) in sara_list:
#         # user_id in sara_list which means unvote for sara and vote for mara
#         sara_list.remove(str(user_id))
#         mara_list.append(str(user_id))

#     else:
#         # user_id not in both of mara or sara which means new
#         mara_list.append(str(user_id))

#     mara_cnt = len(mara_list)
#     sara_cnt = len(sara_list)

#     mara_str = ' '.join(mara_list)
#     sara_str = ' '.join(sara_list)

#     Post.mara = mara_str
#     Post.sara = sara_str

#     # Always return an HttpResponseRedirect after successfully dealing
#     # with POST data. This prevents data from being posted twice if a
#     # user hits the Back button.
#     return HttpResponseRedirect(self.request.path_info)
    # return HttpResponseRedirect('<int:pk>', args=(post.id,))
    # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


# def vote(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     try:
#         selected_choice = post.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the post voting form.
#         return render(request, 'posts/detail.html', {
#             'post': post,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))
#         # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


# js 동적인 내용 표현


def sara_vote(post, user_name):
    post = post
    user_name = user_name.username
    print('@@@@@@@@@@@@@@@@@@@@')

    sara_str = post.sara
    print('sara str')
    print(sara_str)

    mara_str = post.mara
    print('mara str')
    print(mara_str)

    if sara_str is None:
        sara_list = []
    else:
        sara_list = sara_str.split(' ')

    if mara_str is None:
        mara_list = []
    else:
        mara_list = mara_str.split(' ')

    print('sara list before')
    print(sara_list)

    print('mara list before')
    print(mara_list)

    if user_name in sara_list:
        print("1번 콜")
        # user_id in sara_str which means unvote for sara
        sara_list.remove(user_name)

    elif user_name in mara_list:
        print("2번 콜")
        # user_id in mara_list which means unvote for mara and vote for sara
        mara_list.remove(user_name)
        sara_list.append(user_name)

    else:
        print("3번 콜")
        # user_id not in both of sara or mara which means new
        sara_list.append(user_name)

    if '' in sara_list:
        sara_list.remove('')
    if '' in mara_list:
        mara_list.remove('')

    print('sara list after')
    print(sara_list)

    print('mara list after')
    print(mara_list)

    post.sara_cnt = len(sara_list)
    post.mara_cnt = len(mara_list)

    sara_str = ' '.join(sara_list)
    mara_str = ' '.join(mara_list)

    post.sara = sara_str
    post.mara = mara_str

    post.save()


def mara_vote(post, user_name):

    post = post

    user_name = user_name.username

    mara_str = post.mara
    print('mara str')
    print(mara_str)

    sara_str = post.sara
    print('sara str')
    print(sara_str)

    if mara_str is None:
        mara_list = []
    else:
        mara_list = mara_str.split(' ')

    if sara_str is None:
        sara_list = []
    else:
        sara_list = sara_str.split(' ')

    if user_name in mara_list:
        print("1번 콜")
        # user_id in sara_str which means unvote for sara
        mara_list.remove(user_name)

    elif user_name in sara_list:
        print("2번 콜")
        # user_id in mara_list which means unvote for mara and vote for sara
        sara_list.remove(user_name)
        mara_list.append(user_name)

    else:
        print("3번 콜")
        # user_id not in both of sara or mara which means new
        mara_list.append(user_name)

    if '' in mara_list:
        mara_list.remove('')
    if '' in sara_list:
        sara_list.remove('')

    print('sara list after')
    print(sara_list)

    print('mara list after')
    print(mara_list)

    post.mara_cnt = len(mara_list)
    post.sara_cnt = len(sara_list)

    mara_str = ' '.join(mara_list)
    sara_str = ' '.join(sara_list)

    post.mara = mara_str
    post.sara = sara_str

    post.save()
