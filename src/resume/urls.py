from django.conf.urls import url
from resume import views
app_name = 'resume'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^uploadFile/$',views.upload_file,name = 'uploadFile'),
    url(r'^uploadPFile/$', views.upload_file_person, name='uploadPFile'),
]