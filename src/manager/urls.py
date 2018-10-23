from django.conf.urls import url
from manager import views
app_name = 'manager'
urlpatterns = [
#     url(r'^index/$',views.index,name = 'index'),
    url(r'^$',views.index,name = 'manager_index'),
    url(r'^upload/$',views.file_upload,name = 'manager_index'),
    url(r'^bean/$',views.bean_recharge,name = 'manager_index'),
    url(r'^authorize/$',views.authorize,name = 'manager_index')
]