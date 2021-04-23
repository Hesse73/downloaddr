from django.conf.urls import url
from django.views.generic import TemplateView

from . import views #.代表当前目录
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.index1),
    url(r'^index/$', views.index),

    #注册页面
    url(r'^register/$', views.register),

    #登录
    url(r'^login/$', views.login),

    #退出页面
    url(r'^quit/$', views.quit),

    #文件页面
    url(r'^files/$', views.files),

    #上传
    url(r'^upload/$', views.upload),

    #下载
    url(r'^download/$', views.download),
]
