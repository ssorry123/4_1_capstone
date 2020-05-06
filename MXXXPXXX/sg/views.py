from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import ArticleForm
from .models import Article
from .my_function import *


class IndexView(generic.ListView):
    template_name = 'sg/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Article
    template_name = 'sg/detail.html'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now())


def post(request):
    form = ArticleForm()
    ctx = {
        'form': form,
    }
    return render(request, 'sg/post.html', ctx)


def results(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            keyword = request.POST.get('keyword', '')
            ret = generate_3rd(keyword)
            form.text = ret
            ctx = {
                'form': form,
                'ret': ret,
            }
            return render(request, 'sg/post.html', ctx)
    else:
        form = ArticleForm()

    ctx = {
        'form': form,
    }

    return render(request, 'sg/post.html', ctx)


def save(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article()
            article.text = request.POST.get('ret', '')
            article.keyword = form.cleaned_data['keyword']
            article.title = form.cleaned_data['title']
            article.save()
            return redirect('sg:index')

    return redirect('sg:index')
