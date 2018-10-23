from django.conf.urls import url
from company import views
app_name = 'company'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^info/$',views.info,name = 'info'),
]