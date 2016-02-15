from django.conf.urls import include, url
from django.contrib import admin

from django.http import HttpResponse

from . import views

urlpatterns = [
    url(r'abc/$', views.abc),
]