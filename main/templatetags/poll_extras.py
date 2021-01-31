from django import template
from main.models import Comment, SubComment, Post
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='comments')
def comments(post_id):
	comm = []
	post = Post.objects.get(id=int(post_id))
	
	for c in Comment.objects.filter(post=post):
		comm.append([c, SubComment.objects.filter(comment=c)])

	return comm