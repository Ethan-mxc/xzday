from django.conf.urls import url
from online import views
app_name = 'online'
urlpatterns = [
    url(r'^login/$',views.login,name = 'login'),
    url(r'^forget/$',views.forget,name = 'forget'),
    url(r'^register/$',views.register,name = 'register'),
    url(r'^changepasswd/$',views.changepasswd,name = 'changepasswd'),
    url(r'^gotologin/$', views.gotologin, name='gotologin'),
    url(r'^logout', views.logout,name = 'logout'),
    url(r'^getpasswd',views.getpasswd,name = 'getpasswd'),
    url(r'^changehead_image',views.changehead_image,'changehead_image'),
]