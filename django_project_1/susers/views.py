from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
# from .models import Post, Choice
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password


def home(request):
    user_id = request.session.get('user_id')

    if user_id:
        suser = User.objects.get(pk=user_id)
        return HttpResponse(suser.username)

    return HttpResponse(suser.username)


def logout(request):
    if request.session.get('user_id'):
        del(request.session['user_id'])

    return redirect('/posts/')


def login(request):
    if request.method == "GET":
        return render(request, 'susers/login.html')
    elif request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        res_data = {}

        if not(username and password):
            res_data['error'] = "모든값을 입려해주세요."
        else:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                pass
                return redirect('/posts/')
            else:
                res_data['error'] = "비밀번호가 틀렸습니다."

    return render(request, 'susers/login.html', res_data)


def register(request):
    if request.method == "GET":
        return render(request, 'susers/register.html')
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
            user = User.objects.create_user(
                username, email=None, password=password)
        return render(request, 'susers/register.html', res_data)
