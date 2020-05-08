from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth

@require_http_methods(["GET"])
def cac(request):
    response={}
    try:
        response['result']=int(request.GET['i'])+int(request.GET['j'])
        response['res']="结果1"
        response['error_num']=0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
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