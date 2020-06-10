from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import auth
import json

from .models import Writing
from .forms import UserForm, ArticleForm
from .sw_gpt_function import *
from .google_crawling_20026 import collect_links


# 단순히 HTML만 띄우는 코드
def index(request):
    return render(request, 'sg/index.html')


# POST인경우 받아온 데이터를 처리하고 HTML에 넘겨줌
def writing(request):
    if request.method == "POST":
        # HTML에서 값 받아오는 법
        title = request.POST['title']
        content = request.POST['content']
        text = request.POST['text']

        # 문장 생성 함수

        gen = serveral_sentence_generate(content)
        for i in range(len(gen)):
            text = text + gen[i]

        collect = collect_links.CollectLinks()
        links = collect.google_full(title)

        ctx = {
            'title': title,
            'content': '',
            'text': text,
            'links': links,
        }

    else:
        ctx = {
            'title': '',
            'content': '',
            'text': '',
            'links': '',
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


def logout(request):
    auth.logout(request)
    return redirect('sg:index')


def recommend_words(request):
    if request.method == "POST":
        content = request.POST["content"]
        words_list = context_words_list2(content)
        recommend = []
        for i in range(5):
            recommend.append(words_list[i][0][0])
        ctx = {
            'recommend': recommend,
        }
        return HttpResponse(json.dumps(ctx), content_type="application/json")


def detail(request):
    return render(request, 'sg/news_detail.html')


def crawling_images(request):
    if request.method == "POST":
        title = request.POST['title']
        if title == '':
            return redirect('sg:writing')
        collect = collect_links.CollectLinks()
        links = collect.google_full(title)
        context = {
            'links': links,
        }
        return render(request, 'sg/writing.html', context)
    else:
        return redirect('sg:writing')


def list(request):
    # 해당 카테고리인 최신글 10개 디비에서 가져오기
    cat = request.GET.get('cat')
    articles = Writing.objects.filter(category=cat)
    context = {
        'cat': cat,
        'articles': articles,
    }
    return render(request, 'sg/list.html', context)
