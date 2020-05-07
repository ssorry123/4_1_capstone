from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import function
# Create your views here.

#깃풀실험

# 성구형 문장생성있어서 서버 시작 준비시간 단축하기위해 주석처리 2020_05_07_12:16
'''
def index(request):
    ret = 'HELOO GGHH\n'
    sent = '칼을 세워'
    ret1=function.get_one_sentence(sent)
    ret +=sent+' : '
    ret +=ret1
    
    
    return HttpResponse(ret)
'''

def index1(request):
    return HttpResponse("안녕")
