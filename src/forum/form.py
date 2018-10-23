#coding:utf-8
from django import forms
from forum.models import Message, Post

class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('content',)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'column', 'type_name','content')



