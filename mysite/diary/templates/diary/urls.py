from django.conf.urls import include, url
from django.contrib import admin

from django.http import HttpResponse

from .views import abc

urlpatterns = [
    url(r'abc/$', views.abc)]