"""jiuye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views import static
from django.conf import settings
import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^more/', views.more, name='more'),
    url(r'^$', views.indexView, name='index'),
    url(r'^online/', include('online.urls')),
    url(r'^test_one/', include('school.urls',namespace = 'test_one')),
   # url(r'^pay/', include('pay.urls')),
   # url(r'^intr/', include('intr.urls')),
    url(r'^company/', include('company.urls')), 
    url(r'^resume/', include('resume.urls')),
    url(r'^vip/',include('vip.urls',namespace= 'vip')),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^forum/', include('forum.urls')),
    url(r'^person/', include('person.urls')),
   # url(r'^question/', include('question.urls')),
    url(r'^school/', include('school.urls')),
    url(r'^manager/', include('manager.urls')),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static')
]
handler404 = views.page_not_found
handler500 = views.page_not_found