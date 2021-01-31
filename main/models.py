from django.db import models
from django.contrib.auth.models import User

def upload_post_to(instance,filename):
	return f'post_picture/{instance.user.username}/{filename}'

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField()
	picture = models.ImageField(null=True, upload_to = upload_post_to,)
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User,related_name='likes')
	dislikes = models.ManyToManyField(User,related_name='dislikes')



class Like(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)	

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()

class SubComment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	comm = models.TextField()
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)