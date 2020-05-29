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
import TBM_project.myapp.Dp as dpp
import pandas as pd

def adaCost(sample):
    # 可以接受（样本数X特征数）这样的二维ndarray，也可以接受只有一个样本的一维数组（会自动转换为只有一行的二维数组）
    # 输出一个一维ndarray，第i个元素（数字）代表第i个样本预测的围岩等级。
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    f = open(path + '/model/adaCost.pickle', 'rb')
    s = f.read()
    model = pickle.loads(s)
    if len(sample.shape) == 1:
        sample = sample.reshape(1, len(sample))
    return model.predict(sample).tolist()


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
    res = []
    print(json.loads(request.GET['data']))
    for i in json.loads(request.GET['data']):
        p = []
        for j in i:
            p.append(float(j))
        print(p)
        response = RF_CART([p])
        data = [response[0][0], response[1][0]]
        res.append(data)
    return JsonResponse(res, safe=False)


@require_http_methods(["GET"])
def RF3(request):
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    response = {}
    w=json.loads(request.GET['data'])
    file_handle = open(path + '/txtData/1.txt', mode='a')
    file_handle.write(w)
    rf = dpp.RF()
    rf.RFData()
    d=[float(pd.read_csv('data1/train.csv', usecols=['总推进力均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['总推进力方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘功率均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘功率方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘扭矩均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘扭矩方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['推进速度均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['推进速度方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘速度给定均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘速度给定方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘转速均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['刀盘转速方差']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['稳定段刀盘转速均值']).values[0][0]),
       float(pd.read_csv('data1/train.csv', usecols=['稳定段推进速度均值']).values[0][0]),
       ]
    print(d)
    res = RF_CART([d])
    data = [res[0][0], res[1][0]]
    response['prepro']=d
    response['result']=data
    return JsonResponse(response)


@require_http_methods(["GET"])
def AC1(request):
    p = []
    for i in json.loads(request.GET['data']).values():
        p.append(float(i))
    print(p)
    p = np.array(p)
    response = adaCost(p)
    return JsonResponse(response, safe=False)


@require_http_methods(["GET"])
def AC2(request):
    nd=[]
    for i in json.loads(request.GET['data']):
        p = []
        for j in i:
            p.append(float(j))
        print(p)
        nd.append(p)
    nd = np.array(nd)
    response = adaCost(nd)
    return JsonResponse(response, safe=False)


@require_http_methods(["GET"])
def AC3(request):
    response = {}
    w=json.loads(request.GET['data'])
    file_handle = open('txtData/1.txt', mode='w')
    file_handle.write(w)
    rf = dpp.AdaCost()
    rf.adaCostData()
    d=[float(pd.read_csv('data2/adaCostPreData.csv',usecols=['刀盘运行时间均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['撑靴压力均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['刀盘转速均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['撑靴泵压力均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['左撑靴俯仰角均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['控制泵压力均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['右撑靴俯仰角均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['左撑靴滚动角均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['左撑靴油缸行程检测均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['右撑靴滚动角均值']).values[0][0]),
       float(pd.read_csv('data2/adaCostPreData.csv', usecols=['右撑靴油缸行程检测均值']).values[0][0]),
       ]
    print(d)

    w = np.array(d)
    data = adaCost(w)
    response['prepro']=d
    response['result']=data
    return JsonResponse(response)
