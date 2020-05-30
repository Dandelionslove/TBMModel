from django.conf.urls import url,include

from . import views

urlpatterns=[url(r'RF_para',views.RF1,),url(r'AC_para',views.AC1,),url(r'RF_batch',views.RF2,)
             ,url(r'AC_batch',views.AC2,),url(r'RF_file',views.RF3,),url(r'AC_file',views.AC3,),
             url(r'RF_result',views.RF4,),url(r'AC_result',views.AC4,)]