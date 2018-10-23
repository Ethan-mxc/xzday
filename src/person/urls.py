from django.conf.urls import url
from person import views
app_name = 'person'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^index2/$', views.index2, name='index2'),
    url(r'^info/$',views.info,name = 'info'),
    url(r'^test/$',views.test,name = 'test'),
]