from django.conf.urls import url
from intr import views
app_name = 'intr'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^info/$',views.info,name = 'info'),
    url(r'^money/$',views.money,name = 'money'),
]