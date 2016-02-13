# Shelby Mahaffie

"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.http import HttpResponse

def abc(request):
    path = request.path

    return HttpResponse('''
        </h1>Title</h1>
        <p>Welcome! You came to {}.</p>'''.format(path))

# It tries to match, if it doesn't match, it continues.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^abc', abc),
    url(r'^$', abc),

    # If we match 'start with diary', we're going to
    # send it to another url dispatcher
    url(r'^diary/', include('diary.urls'))

    ]
