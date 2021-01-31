from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages
import random
from .models import UserOTP, Profile, Notification
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from main.models import Post

def signup(request):
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				messages.success(request, f'Account is Created For {usr.username}')
				return redirect('login')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'user/signup.html', {'otp': True, 'usr': usr})

		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			name = form.cleaned_data.get('name').split(' ')

			usr = User.objects.get(username=username)
			usr.email = username
			usr.first_name = name[0]
			if len(name) > 1:
				usr.last_name = name[1]
			usr.is_active = False
			usr.save()
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)

			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to ITScorer - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)

			return render(request, 'user/signup.html', {'otp': True, 'usr': usr})

		
	else:
		form = SignUpForm()

	return render(request, 'user/signup.html', {'form':form})


def resend_otp(request):
	if request.method == "GET":
		get_usr = request.GET['usr']
		if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
			usr = User.objects.get(username=get_usr)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to ITScorer - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return HttpResponse("Resend")

	return HttpResponse("Can't Send ")


def login_view(request):
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':
		get_otp = request.POST.get('otp') #213243 #None

		if get_otp:
			get_usr = request.POST.get('usr')
			usr = User.objects.get(username=get_usr)
			if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
				usr.is_active = True
				usr.save()
				login(request, usr)
				return redirect('home')
			else:
				messages.warning(request, f'You Entered a Wrong OTP')
				return render(request, 'user/login.html', {'otp': True, 'usr': usr})


		usrname = request.POST['username']
		passwd = request.POST['password']

		user = authenticate(request, username = usrname, password = passwd) #None
		if user is not None:
			login(request, user)
			return redirect('home')
		elif not User.objects.filter(username = usrname).exists():
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('login')
		elif not User.objects.get(username=usrname).is_active:
			usr = User.objects.get(username=usrname)
			usr_otp = random.randint(100000, 999999)
			UserOTP.objects.create(user = usr, otp = usr_otp)
			mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

			send_mail(
				"Welcome to ITScorer - Verify Your Email",
				mess,
				settings.EMAIL_HOST_USER,
				[usr.email],
				fail_silently = False
				)
			return render(request, 'user/login.html', {'otp': True, 'usr': usr})
		else:
			messages.warning(request, f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
			return redirect('login')

	form = AuthenticationForm()
	return render(request, 'user/login.html', {'form': form})

# User Profile View
def profile(request, username):
	user = User.objects.filter(username=username)
	if not user:
		raise Http404()
	if request.user == user.first():
		if request.method == 'POST':
			passChangeForm = PasswordChangeForm(request.user, request.POST)
			if passChangeForm.is_valid():
				passChangeForm.save()
				messages.success(request, f'Password had been changed successfully')
		else:
			passChangeForm = PasswordChangeForm(request.user)
		parms = {
			'passChangeForm' : passChangeForm,
			'useritself': True,
			'user': request.user
			}
		# return render(request, 'user/profile.html', parms)
	else:
		parms = {
			'useritself': False,
			'user': user.first(),
		}

	posts = Post.objects.filter(user = user.first()).order_by('-created_at')

	all_post = Paginator(posts,10)
	page = request.GET.get('page')
	try:
		posts = all_post.page(page)
	except PageNotAnInteger:
		posts = all_post.page(1)
	except EmptyPage:
		posts = all_post.page(all_post.num_pages)

	parms['posts'] = posts
	return render(request, 'user/profile.html', parms)

# This view is used to change profile pic, cover image, about, dob and more user details
@login_required
def ChangeIntoProfile(request, fieldname):
	prof = request.user.profile

	#Change Profile Picture
	if fieldname == 'profile_pic':
		img = request.FILES.get('profile_pic')
		if img:
			prof.profile_pic = img
			prof.save()
		return redirect(f"/user/{request.user}")
	# Change Cover Image
	elif fieldname == 'cover_image':
		img = request.FILES.get('cover_image')
		if img:
			prof.cover_image = img
			prof.save()
		return redirect(f"/user/{request.user}")


	value = request.GET.get('value')
	if not value:
		raise Http404()
	# print(value, fieldname)

	# Change Name
	if fieldname == 'name':
		name = value.split(' ')
		request.user.first_name = name[0]
		if len(name) > 1:
			request.user.last_name = name[1]
		request.user.save()
	# Change About Me
	elif fieldname == 'aboutme':
		prof.about_me = value
		prof.save()
	#Change Date of Birth
	elif fieldname == 'dob':
		prof.birthday = value
		prof.save()
	#Change Gender
	elif fieldname == 'gender':
		if value == "Male":
			prof.gender = "Male"
			prof.save()
		elif value == "Female":
			prof.gender = 'Female'
			prof.save()
		elif value == "Other":
			prof.gender = "Other"
			prof.save()
	else:
		raise Http404()
	return HttpResponse(value)

@login_required
@csrf_exempt
def following(request):
	if request.method == 'POST' and request.user.is_authenticated:
		data = {}
		for usr in request.user.profile.following.all():
			data[usr.id] = {
			 'first_name' : usr.first_name,
			 'last_name': usr.last_name,
			 'username' : usr.username,
			 'pic' : usr.profile.profile_pic.url
			 }
		
		return JsonResponse(data)
	raise Http404()

@login_required
@csrf_exempt
def followers(request):
	if request.method == 'POST' and request.user.is_authenticated:
		data = {}
		for usr in request.user.profile.followers.all():
			data[usr.id] = {
			 'first_name' : usr.first_name,
			 'last_name': usr.last_name,
			 'username' : usr.username,
			 'pic' : usr.profile.profile_pic.url,
			 'followed_back': usr in request.user.profile.following.all()
			 }
		
		return JsonResponse(data)
	raise Http404()

@login_required
def notifications(request):
	noti = Notification.objects.filter(user=request.user, seen = False)
	noti = serializers.serialize('json', noti)
	return JsonResponse({'data':noti})

@login_required
def notifications_seen(request):
	Notification.objects.filter(user=request.user, seen = False).update(seen = True)
	return HttpResponse(True)

@csrf_exempt
@login_required
def clear_notifications(request):
	if request.method == "POST":
		Notification.objects.filter(user=request.user).delete()
		return HttpResponse(True)
	return HttpResponse(False)

def islogin(request):
	return JsonResponse({'is_login':request.user.is_authenticated})