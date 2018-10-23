from django.conf.urls import url
from question import views
app_name = 'question'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^info/$',views.info,name = 'info'),
    url(r'^list/$',views.list,name = 'list'),
]