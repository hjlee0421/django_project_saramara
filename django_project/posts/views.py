from .models import Post, User, Comment

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.views import generic, View
from django.views.generic.edit import FormMixin

from .forms import PostForm

from django.core.paginator import Paginator


# There is Q objects that allow to complex lookups. Example:
# Item.objects.filter(Q(creator=owner) | Q(moderated=False))
from django.db.models import Q

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


class IndexView(generic.ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'post_objects'
    paginate_by = 10

    # def get_queryset(self):
    # return Post.objects.all()

    def get(self, request, *args, **kwargs):
        print('hello')
        keyword = request.GET.get('keyword')
        category = request.GET.get('category')
        category_list = ['상의', '하의', '신발', '기타']

        if category in category_list:
            self.queryset = self.get_queryset().filter(category=category)
        if keyword:
            # Item.objects.filter(Q(creator=owner) | Q(moderated=False))
            self.queryset = self.get_queryset().filter(Q(title__icontains=keyword)
                                                       | Q(ckcontent__icontains=keyword))
            # filter 적용한 부분
            # TODO : filter 여러가지 기능 추가하기
            # https://docs.djangoproject.com/en/3.1/ref/models/querysets/
            # 위 주소에 다양한 필터 기능 있음
            # 쭉 살펴봐야 할듯
            # css부분 작업
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

        context = self.get_context_data(object=self.object)

        context['comment'] = self.object.comment_set.all()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        user_id = request.session.get('user_id')
        suser = User.objects.get(pk=user_id)

        post = Post(author=suser, title='test for POST')

        if 'delete_comment_button' in request.POST:
            comment_id = request.POST['delete_comment']
            comment = Comment.objects.get(id=comment_id)
            if suser == comment.author:
                comment.delete()

        self.object = self.get_object()

        context = self.get_context_data(object=self.object)

        if 'sara_button' in request.POST:
            self.sara_vote(suser)
        elif 'mara_button' in request.POST:
            self.mara_vote(suser)
        elif 'add_comment' in request.POST:
            self.add_comment(suser, request.POST.get('add_comment'))
        context['comment'] = self.object.comment_set.all()
        return self.render_to_response(context)

    def add_comment(self, user_name, user_comment):
        post = self.object
        user_name = user_name
        comment = Comment(post=post, author=user_name, text=user_comment)
        comment.save()

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
            suser = User.objects.get(pk=user_id)
            post = Post(**form.cleaned_data)
            post.author = suser
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
            del(request.session['user_id'])

        logout(request)

        return redirect('/')


class MypageView(View):
    def get(self, request):
        return render(request, 'posts/mypage.html')
