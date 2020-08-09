from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from .models import Post, Choice
from django.urls import reverse
from django.views import generic
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


class IndexView(generic.ListView):
    template_name = 'posts/index.html'
    context_object_name = 'latest_post_list'

    def get_queryset(self):
        return Post.objects.all()


class DetailView(generic.DeleteView):
    model = Post
    template_name = 'posts/detail.html'


class ResultsView(generic.DetailView):
    model = Post
    template_name = 'posts/results.html'


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
