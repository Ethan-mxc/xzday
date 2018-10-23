from django.conf.urls import url
from forum.views import *
from forum import *
app_name = 'forum'
urlpatterns = [
    url(r'index',index.as_view(),name='index'),
    url(r'^columns/$',views.columnall,name='column_all'),
    url(r'^column/(?P<column_pk>\d+)/$',views.columndetail,name='column_detail'),
    url(r'^postdetail/(?P<post_pk>\d+)/$', views.postdetail, name='post_detail'), 
    url(r'^postlist/$', UserPostView.as_view(), name='user_post'),
    url(r'^post_create/$', PostCreate.as_view(), name='post_create'), 
    url(r'^post_update/(?P<pk>\d+)/$', PostUpdate.as_view(), name='post_update'),       
    url(r'^post_delete/(?P<pk>\d+)/$', PostDelete.as_view(), name='post_delete'), 
    url(r'^search/$', SearchView.as_view(), name='search'),
]