from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .forms import KeywordForm
from .models import Keyword
from .my_function import *


def indexView(request):
    if request.method == "POST":
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword_text = request.POST.get('keyword_text', '')
            ret = generate_3rd(keyword_text)
            keyword_obj = Keyword(keyword_text=ret)
            # keyword_obj.save()
            ctx = {
                'keyword': ret,
            }
            return render(request, 'practice/results.html', ctx)
    else:
        form = KeywordForm()

    ctx = {
        'form': form,
    }

    return render(request, 'practice/index.html', ctx)


class ResultsView(generic.DetailView):
    model = Keyword
    template_name = '/results.html'
