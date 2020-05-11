from django.shortcuts import render
import json
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth
import joblib
import os
import sys
import pickle
import numpy as np


def adaCost(sample):
    # 可以接受（样本数X特征数）这样的二维ndarray，也可以接受只有一个样本的一维数组（会自动转换为只有一行的二维数组）
    # 输出一个一维ndarray，第i个元素（数字）代表第i个样本预测的围岩等级。
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    f = open(path + '/model/adaCost.pickle', 'rb')
    s = f.read()
    model = pickle.loads(s)
    if len(sample.shape) == 1:
        sample = sample.reshape(1, len(sample))
    return model.predict(sample)


def RF_CART(data):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    clf_f = joblib.load(path + '/model/model_f.pkl')
    clf_t = joblib.load(path + '/model/model_t.pkl')
    result_t = clf_t.predict(data)
    result_f = clf_f.predict(data)
    return [result_t, result_f]


@require_http_methods(["GET"])
def RF1(request):
    p = []
    for i in json.loads(request.GET['data']).values():
        p.append(float(i))
    print(p)
    response = RF_CART([p])
    data = [response[0][0], response[1][0]]
    return JsonResponse(data, safe=False)


@require_http_methods(["GET"])
def RF2(request):
    response = {}
    try:
        response['result'] = int(request.GET['i']) - int(request.GET['j'])
        response['res'] = "结果1"
        response['error_num'] = 10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def RF3(request):
    response = {}
    try:
        response['result'] = int(request.GET['i']) - int(request.GET['j'])
        response['res'] = "结果1"
        response['error_num'] = 10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def AC1(request):
    p = []
    for i in json.loads(request.GET['data']).values():
        p.append(float(i))
    print(p)
    p = np.array(p)
    response = adaCost(p)
    return JsonResponse(response)


@require_http_methods(["GET"])
def AC2(request):
    response = {}
    try:
        response['result'] = int(request.GET['i']) - int(request.GET['j'])
        response['res'] = "结果1"
        response['error_num'] = 10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def AC3(request):
    response = {}
    try:
        response['result'] = int(request.GET['i']) - int(request.GET['j'])
        response['res'] = "结果1"
        response['error_num'] = 10
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
