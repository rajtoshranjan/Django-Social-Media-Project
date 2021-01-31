from django.db import models
from django.contrib.auth.models import User
from PIL import Image
class UserOTP(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	time_st = models.DateTimeField(auto_now = True)
	otp = models.SmallIntegerField()

def upload_profile_to(instance,filename):
	return f'profile_picture/{instance.user.username}/{filename}'

def upload_cover_to(instance,filename):
	return f'coverImage/{instance.user.username}/{filename}'

class Profile(models.Model):
	gen = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	about_me = models.CharField(max_length=250, null=True)
	birthday = models.DateField(null=True)
	profile_pic = models.ImageField(upload_to = upload_profile_to, null=True, default = 'defaults/profile_pic.jpg')
	cover_image = models.ImageField(upload_to = upload_cover_to, null = True, default= 'defaults/cover_image.jpg')
	gender = models.CharField(choices=gen, max_length=6, null=True)
	followers = models.ManyToManyField(User, related_name='followers', blank=True)
	following = models.ManyToManyField(User, related_name="following", blank=True)

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.profile_pic.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.profile_pic.path)

		img2 = Image.open(self.cover_image.path)
		if img2.height > 500 or img2.width > 500:
			output_size = (500, 500)
			img2.thumbnail(output_size)
			img2.save(self.cover_image.path)

	def non_followed_user(self):
		return set(User.objects.filter(is_active=True))-set(self.following.all())-{self.user}

	def get_notifications(self):
		return Notification.objects.filter(user=self.user, seen = False)

class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.CharField(max_length=500)
	link = models.CharField(max_length=500)
	seen = models.BooleanField(default=False)

