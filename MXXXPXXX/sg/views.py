from django.shortcuts import render, get_object_or_404
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
        """
        Return the last five published questions (not
        including those set to be
        published in the future).
        """
        return Article.objects.filter(
            pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


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
            keyword_obj = Article(text=ret)
            # keyword_obj.save()
            ctx = {
                'ret': ret,
            }
            return render(request, 'sg/results.html', ctx)
    else:
        form = ArticleForm()

    ctx = {
        'form': form,
    }

    return render(request, 'sg/post.html', ctx)


def save(request):
    if request.method == "POST":
        return render(request, 'sg/index.html')
    else:
        return render(request, 'sg/index.html')