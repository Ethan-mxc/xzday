from django.conf.urls import url
from school import views
app_name = 'school'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^info/$',views.info,name = 'info'),
    url(r'^all/$',views.all,name = 'all'),
    url(r'^test_one/$', views.test_one, name='test_one'),
]
