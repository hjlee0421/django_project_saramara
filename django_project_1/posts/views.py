from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Post, Choice
from django.urls import reverse
from django.views import generic
from .forms import PostForm
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import User


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.all()  # .order_by('-id')


class DetailView(generic.DeleteView):
    model = Post
    template_name = 'posts/detail.html'


class ResultsView(generic.DetailView):
    model = Post
    template_name = 'posts/results.html'


# copy and change sara <> mara
# ADD LOGIN STEP
# add @login_required
def sara_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    user_id = request.session.get('user_id')

    sara_str = post.sara
    mara_str = post.mara

    # check textfield is empty or not and create list
    if not sara_str:
        sara_list = sara_str.split(' ')
    else:
        sara_list = []

    if not mara_str:
        mara_list = mara_str.split(' ')
    else:
        mara_list = []

    if str(user_id) in sara_list:
        # user_id in sara_str which means unvote for sara
        sara_list.remove(str(user_id))

    elif str(user_id) in mara_list:
        # user_id in mara_list which means unvote for mara and vote for sara
        mara_list.remove(str(user_id))
        sara_list.append(str(user_id))

    else:
        # user_id not in both of sara or mara which means new
        sara_list.append(str(user_id))

    sara_cnt = len(sara_list)
    mara_cnt = len(mara_list)

    sara_str = ' '.join(sara_list)
    mara_str = ' '.join(mara_list)

    Post.sara = sara_str
    Post.mara = mara_str

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))
    # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


# copy and change sara <> mara
# ADD LOGIN STEP
# add @login_required
def mara_vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    user_id = request.session.get('user_id')

    mara_str = post.mara
    sara_str = post.sara

    # check textfield is empty or not and create list
    if not mara_str:
        mara_list = mara_str.split(' ')
    else:
        mara_list = []

    if not sara_str:
        sara_list = sara_str.split(' ')
    else:
        sara_list = []

    if str(user_id) in mara_list:
        # user_id in mara_str which means unvote for mara
        mara_list.remove(str(user_id))

    elif str(user_id) in sara_list:
        # user_id in sara_list which means unvote for sara and vote for mara
        sara_list.remove(str(user_id))
        mara_list.append(str(user_id))

    else:
        # user_id not in both of mara or sara which means new
        mara_list.append(str(user_id))

    mara_cnt = len(mara_list)
    sara_cnt = len(sara_list)

    mara_str = ' '.join(mara_list)
    sara_str = ' '.join(sara_list)

    Post.mara = mara_str
    Post.sara = sara_str

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))
    # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


def vote(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    try:
        selected_choice = post.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the post voting form.
        return render(request, 'posts/detail.html', {
            'post': post,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('posts:detail', args=(post.id,)))
        # return HttpResponseRedirect(reverse('posts:results', args=(post.id,)))


def mypage(request):
    return render(request, 'posts/mypage.html')


@login_required
def ask(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user_id')
            suser = User.objects.get(pk=user_id)
            post = Post()
            post.title = form.cleaned_data['title']
            post.brand = form.cleaned_data['brand']
            post.price = form.cleaned_data['price']
            post.link = form.cleaned_data['link']
            post.content = form.cleaned_data['content']

            post.author = suser
            post.save()
            return redirect('/posts/')
        else:
            return redirect('/posts/')
    else:
        form = PostForm()

    return render(request, 'posts/item_ask.html', {'form': form})
