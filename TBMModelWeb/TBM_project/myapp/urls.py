from django.conf.urls import url,include

from . import views

urlpatterns=[url(r'RF_para',views.RF1,),url(r'AdaCost_para',views.AC1,)]