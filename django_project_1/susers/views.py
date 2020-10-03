from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from posts.models import User  # create new user

from .forms import UserForm
from .forms import LoginForm

# def signup(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             new_user = User.objects.create_user(**form.cleaned_data)
#             login(request, new_user)
#             return redirect('/posts/')
#     else:
#         form = UserForm()
#         return render(request, 'susers/register.html')


def signup(request):
    if request.method == "GET":
        return render(request, 'susers/signup.html')
    elif request.method == "POST":
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

        return render(request, 'susers/signup.html', res_data)


# def home(request):
#     # user_id = request.session.get('user_id')

#     # if user_id:
#     #     suser = User.objects.get(pk=user_id)
#     #     return HttpResponse(suser.username)

#     # return HttpResponse(suser.username)
#     return redirect('/')


def signout(request):
    if request.session.get('user_id'):
        del(request.session['user_id'])

    logout(request)

    return redirect('/')


# def signout(request):
#     logout(request)
#     return redirect('/posts/')


def signin(request):
    if request.method == "GET":
        return render(request, 'susers/signin.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}

        if not(username and password):
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

    return render(request, 'susers/signin.html', res_data)


# def signin(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         res_data = {}

#         if user is not None:
#             login(request, user)
#             return redirect('/posts/')
#         else:
#             res_data['error'] = "비밀번호가 틀렸습니다."
#             # return HttpResponse('Login failed. Try again.')
#     else:
#         form = LoginForm()
#         return render(request, 'susers/login.html')

#     return render(request, 'susers/login.html', res_data)
