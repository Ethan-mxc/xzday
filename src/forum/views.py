#-*-coding:utf-8-*-
from forum.models import Nav, Post, Comment, Application,  Column, Message
from django.views.generic import View,TemplateView,ListView,DetailView
from django.utils.timezone import now, timedelta
from datetime import datetime
from django.core.cache import cache
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from online.models import *
from form import MessageForm, PostForm
from django.db.models import Q

PAGE_NUM = 50
class BaseMixin(object):
    def get_context_data(self,*args,**kwargs):
        context = super(BaseMixin,self).get_context_data(**kwargs)
        try:
            context['nav_list'] =  Nav.objects.all()
            context['column_list'] = Column.objects.all()[0:5]
            context['last_comments'] = Comment.objects.all().order_by("-created_at")[0:10]
        except Exception as e:
            print u'[BaseMixin]加载基本信息出错'

        return context

#首页
class index(BaseMixin,ListView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'forumindex.html'
    context_object_name = 'post_list'
    paginate_by = PAGE_NUM #分页--每页的数目
    def get_context_data(self,**kwargs):
        kwargs['foruminfo'] =get_forum_info()
        kwargs['online_ips_count'] =get_online_ips_count()
        kwargs['hot_posts'] = self.queryset.order_by("-responce_times")[0:10]       
        return super(index,self).get_context_data(**kwargs)
        
    
#得到论坛信息，贴子数，用户数，昨日发帖数，今日发帖数
def get_forum_info():
    #请使用缓存
    oneday = timedelta(days=1)
    today = now().date()
    lastday = today - oneday
    todayend = today + oneday
    post_number = Post.objects.count()

    lastday_post_number = cache.get('lastday_post_number', None)
    today_post_number = cache.get('today_post_number', None)

    if lastday_post_number is None:
        lastday_post_number = Post.objects.filter(created_at__range=[lastday,today]).count()
        cache.set('lastday_post_number',lastday_post_number,60*60)
    
    if today_post_number is None:
        today_post_number = Post.objects.filter(created_at__range=[today,todayend]).count()
        cache.set('today_post_number',today_post_number,60*60)

    info = {"post_number":post_number,
        "lastday_post_number":lastday_post_number,
        "today_post_number":today_post_number}
    return info

def get_online_ips_count():
    online_ips = cache.get("online_ips", [])
    if online_ips:
        online_ips = cache.get_many(online_ips).keys()
        return len(online_ips)
    return 0

#帖子
def postdetail(request,post_pk):
    post_pk = int(post_pk)
    post = Post.objects.get(pk=post_pk)
    comment_list = post.comment_set.all()    
    #统计帖子的访问访问次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    title = post.title
    visited_ips = cache.get(title, [])

    if ip not in visited_ips:
        post.view_times += 1
        post.save()
        visited_ips.append(ip)
    cache.set(title,visited_ips,15*60)
    return render_to_response('post_detail.html',{'post':post,'comment_list':comment_list})
#用户已发贴
class UserPostView(ListView):
    template_name = 'user_posts.html'
    context_object_name = 'user_posts'
    paginate_by = PAGE_NUM

    def get_queryset(self):
        user_posts = Post.objects.filter(author=self.request.user)
        return user_posts


#发帖
class PostCreate(CreateView):   
    model = Post
    template_name = 'form.html'
    form_class = PostForm
    #fields = ('title', 'column', 'type_name','content')
    #SAE django1.5中fields失效，不知原因,故使用form_class
    success_url = reverse_lazy('user_post')
    #这里我们必须使用reverse_lazy() 而不是reverse，因为在该文件导入时URL 还没有加载。

    def form_valid(self, form):
        #此处有待加强安全验证
        validate = self.request.POST.get('validate',None)
        formdata = form.cleaned_data
        if self.request.session.get('validate',None) != validate:
            return HttpResponse("验证码错误！<a href='/'>返回</a>")
        user = User.objects.get(username=self.request.user.username)
        #form.instance.author = user
        #form.instance.last_response  = user
        formdata['author'] = user
        formdata['last_response'] = user
        p = Post(**formdata)
        p.save()
        user.levels += 5    #发帖一次积分加 5
        user.save()
        return HttpResponse("发贴成功！<a href='/'>返回</a>")
     
#编辑贴
class PostUpdate(UpdateView):   
    model = Post
    template_name = 'form.html'
    success_url = reverse_lazy('user_post')             


#删贴
class PostDelete(DeleteView):
    model = Post
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('user_post')  
#所有板块
def columnall(request):
    column_list = Column.objects.all()
    return render_to_response('column_list.html',{'column_list':column_list })

#每个板块
def columndetail(request,column_pk):
    column_obj = Column.objects.get(pk=column_pk)
    column_posts = column_obj.post_set.all()
    
    return render_to_response('column_detail.html',{'column_obj':column_obj,'column_posts':column_posts },context_instance=RequestContext(request))  
#搜索 
class SearchView(ListView):
    template_name = 'search_result.html'
    context_object_name = 'post_list'
    paginate_by = PAGE_NUM

    def get_context_data(self,**kwargs):
        kwargs['q'] = self.request.GET.get('srchtxt','')
        return super(SearchView,self).get_context_data(**kwargs)

    def get_queryset(self):
        #获取搜索的关键字
        q = self.request.GET.get('srchtxt','')
        #在帖子的标题和内容中搜索关键字
        post_list = Post.objects.only('title','content').filter(Q(title__icontains=q)|Q(content__icontains=q));
        return post_list
