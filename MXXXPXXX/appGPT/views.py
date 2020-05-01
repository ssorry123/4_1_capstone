from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import function
# Create your views here.

def index(request):
    ret = 'HELOO GGHH\n'
    sent = '칼을 세워'
    ret1=function.get_one_sentence(sent)
    ret +=sent+' : '
    ret +=ret1
    
    
    return HttpResponse(ret)