from django.shortcuts import render
import json
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth
import joblib
import os
import sys


def RF_CART(data):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    clf_f = joblib.load(path + '/model/model_f.pkl')
    clf_t = joblib.load(path + '/model/model_t.pkl')
    result_t = clf_t.predict(data)
    result_f = clf_f.predict(data)
    return [result_t, result_f]

@require_http_methods(["GET"])
def RF1(request):
    p=[]
    for i in json.loads(request.GET['data']).values():
        p.append(float(i))
    print(p)
    response=RF_CART(p)
    return JsonResponse(response)

@require_http_methods(["GET"])
def cac2(request):
    response={}
    try:
        response['result']=int(request.GET['i'])-int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def cac3(request):
    response={}
    try:
        response['result']=int(request.GET['i'])-int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def cac4(request):
    response={}
    try:
        response['result']=int(request.GET['i'])-int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def cac5(request):
    response={}
    try:
        response['result']=int(request.GET['i'])-int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)

@require_http_methods(["GET"])
def cac6(request):
    response={}
    try:
        response['result']=int(request.GET['i'])-int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)