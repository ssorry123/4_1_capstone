from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth

from .models import Writing
from .forms import UserForm, ArticleForm
from .sw_gpt_function import *


# 단순히 HTML만 띄우는 코드
def index(request):
    return render(request, 'sg/index.html')


# POST인경우 받아온 데이터를 처리하고 HTML에 넘겨줌
def writing(request):
    if request.method == "POST":
        # HTML에서 값 받아오는 법
        title = request.POST['title']
        content = request.POST['content']
        # 문장 생성 함수
        text = serveral_sentence_generate(content)
        ctx = {
            'title': title,
            'content': content,
            'text': text,
        }
    else:
        ctx = {
            'title': '',
            'content': '',
            'text': '',
        }
    return render(request, 'sg/writing.html', ctx)


# DB에 저장하고 index페이지로 이동
def save(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sg:index')
    return redirect('sg:writing')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('sg:index')
        else:
            return HttpResponse(form.errors)

    else:
        form = UserForm()
        return render(request, 'sg/signup.html', {'form': form})


def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        user = auth.authenticate(request, username=userid, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('sg:index')
        else:
            return render(request, 'sg/login.html',
                          {'error': 'userid or password is incorrect'})

    else:
        return render(request, 'sg/login.html')
