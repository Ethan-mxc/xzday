from django.conf.urls import url
from vip import views
app_name = 'vip'
urlpatterns = [
    url(r'^index/$',views.index,name = 'index'),
    url(r'^search/$',views.search,name = 'search'),
    url(r'^share_search/$',views.share_search,name = 'share_search'),
    url(r'^delete/(?P<res_id>[0-9]+)$', views.delete, name='delete'),
    url(r'^order_delete/(?P<res_id>[0-9]+)$', views.order_delete, name='order_delete'),
    url(r'^vip_edit/(?P<res_id>[0-9]+)$',views.vip_edit,name='vip_edit'),
    url(r'^order_edit/(?P<res_id>[0-9]+)$', views.order_edit, name='order_edit'),
    url(r'^show/(?P<res_id>[0-9]+)$', views.show, name='show'),
    url(r'^order_show/(?P<res_id>[0-9]+)$', views.order_show, name='order_show'),
    url(r'^vip_edit/action$',views.vip_edit_action,name='vip_edit_action'),
    url(r'^order_edit/action$', views.order_edit_action, name='order_edit_action')
]
