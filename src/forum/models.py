#coding:utf-8
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from online.models import *
import datetime
from django.core.urlresolvers import reverse
# Create your models here.

class Nav(models.Model):
    name = models.CharField(max_length=40,verbose_name=u'导航条')
    url = models.CharField(max_length=200,blank=True,null=True,verbose_name=u'指向地址')
    create_time = models.DateTimeField(u'创建时间',default=datetime.datetime.now)
    class Meta:
        db_table = 'nav'
        verbose_name_plural = verbose_name = u"导航条"
        ordering = ['-create_time']

    def __unicode__(self):
        return self.name    

class Column(models.Model):                            #板块
    name = models.CharField(max_length=30)
    description = models.TextField()
    img = models.CharField(max_length=200,default='/static/tx/default.jpg',verbose_name=u'图标')
    post_number = models.IntegerField(default=0)     #主题数
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'column'
        ordering = ['-post_number']
        verbose_name_plural = u'板块'
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "../../forum"+reverse('column_detail',urlconf = "forum.urls",kwargs={'column_pk': self.pk })
        
class PostType(models.Model):            #文章类型
    type_name = models.CharField(max_length=30)
    description = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    class Meta:
        db_table = 'posttype'
        verbose_name_plural = u'主题类型'
    def __unicode__(self):
        return self.type_name

class Post(models.Model):                    #文章
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User,related_name='post_author')                #作者
    column = models.ForeignKey(Column)                        #所属板块
    type_name = models.ForeignKey(PostType)                        #文章类型
    content = models.TextField()
    
    view_times = models.IntegerField(default=0)        #浏览次数
    responce_times = models.IntegerField(default=0)        #回复次数
    last_response = models.ForeignKey(User)                            #最后回复者
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    
    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
        verbose_name_plural = u'主题'
        
    def __unicode__(self):
        return self.title
    
    def description(self):
        return u'%s 发表了主题《%s》' % (self.author, self.title)
    
    def get_absolute_url(self):
        return "../../forum"+reverse('post_detail',urlconf = "forum.urls",kwargs={'post_pk': self.pk })
        
       
class Comment(models.Model):                #评论    
    post = models.ForeignKey(Post)                        
    author = models.ForeignKey(User)                        
    comment_parent = models.ForeignKey('self', blank=True, null=True,related_name='childcomment')                        
    content = models.TextField()
   
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'comment'
        ordering = ['created_at']
        verbose_name_plural = u'评论'
        
    def __unicode__(self):
        return self.content

    def description(self):
        return u'%s 回复了您的帖子(%s) R:《%s》' % (self.author,self.post, self.content)
    
    def get_absolute_url(self):
        return "../../forum"+reverse('post_detail',urlconf = "forum.urls",kwargs= { 'post_pk': self.post.pk })
        
class Message(models.Model):            #好友消息
    sender = models.ForeignKey(User,related_name='message_sender')                            #发送者
    receiver = models.ForeignKey(User,related_name='message_receiver')                        #接收者
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def description(self):
        return u'%s 给你发送了消息《%s》' % (self.sender, self.content)

    class Meta:
        db_table = 'message'
        verbose_name_plural = u'消息'
    
class Application(models.Model):            #好友申请
    sender = models.ForeignKey(User,related_name='appli_sender')                            #发送者
    receiver = models.ForeignKey(User,related_name='appli_receiver')                        #接收者
    status = models.IntegerField(default=0)                #申请状态 0:未查看 1:同意 2:不同意
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def description(self):
        return u'%s 申请加好友' % self.sender   

    class Meta:
        db_table = 'application'
        verbose_name_plural = u'好友申请'
    


    
    




