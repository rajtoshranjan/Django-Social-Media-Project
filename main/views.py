from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from user.models import Notification
from .models import Post, Like, Dislike, Comment, SubComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

@login_required
def home(request):
	if request.method == "POST":
		text = request.POST.get('text')
		img = request.FILES.get('post_image')
		post = Post(user = request.user, text = text, picture=img)
		post.save()
		mess = f"{request.user.first_name} {request.user.last_name} added a Post."
		for usr in request.user.profile.followers.all():
			noti = Notification(user = usr, message=mess, link = f"/#post{post.id}")
			noti.save()
		return redirect('home')

	following_users = list(request.user.profile.following.all())
	following_users.append(request.user)
	posts = Post.objects.filter(user__in = following_users).order_by('-created_at')

	all_post = Paginator(posts,10)
	page = request.GET.get('page')
	try:
		posts = all_post.page(page)
	except PageNotAnInteger:
		posts = all_post.page(1)
	except EmptyPage:
		posts = all_post.page(all_post.num_pages)

	parms = {
		'non_followed_user': request.user.profile.non_followed_user,
		'posts': posts,
	}
	return render(request, 'main/home.html', parms)

@login_required
@csrf_exempt
def post(request, id=None):
	if request.method == "POST":
		order = request.POST.get('order')
		post_id = int(request.POST.get('post'))
		if order == 'delete':
			Post.objects.get(id=post_id, user=request.user).delete()
			return HttpResponse('deleted')

		elif order == 'like':
			post = Post.objects.get(id=post_id)
			if request.user in post.dislikes.all():
				post.dislikes.remove(request.user)
				try:
					Dislike.objects.filter(user = request.user, post = post)[0].delete()
				except:
					pass
			post.likes.add(request.user)
			Like.objects.create(user=request.user, post=post)
			return HttpResponse('liked')

		elif order == 'dislike':
			post = Post.objects.get(id=post_id)
			if request.user in post.likes.all():
				post.likes.remove(request.user)
				try:
					Like.objects.filter(user = request.user, post = post)[0].delete()
				except:
					pass
			post.dislikes.add(request.user)
			Dislike.objects.create(user=request.user, post=post)
			return HttpResponse('disliked')

		elif order == 'like-back':
			post = Post.objects.get(id=post_id)
			if request.user in post.likes.all():
				post.likes.remove(request.user)
				try:
					Like.objects.filter(user = request.user, post = post)[0].delete()
				except:
					pass
				return HttpResponse('like-backed')

		elif order == 'dislike-back':
			post = Post.objects.get(id=post_id)
			if request.user in post.dislikes.all():
				post.dislikes.remove(request.user)
				try:
					Dislike.objects.filter(user = request.user, post = post)[0].delete()
				except:
					pass
				return HttpResponse('dislike-backed')
		raise Http404()
	raise Http404()

@login_required
@csrf_exempt
def follow(request):
	if request.method == "POST":
		usrname = request.POST.get('user')
		following = get_object_or_404(User, username = usrname)
		following.profile.followers.add(request.user)
		request.user.profile.following.add(following)
		mess = f"{request.user.first_name} {request.user.last_name} started following you."
		noti = Notification(user = following, message=mess, link = f"/user/{request.user.username}")
		noti.save()
		return HttpResponse(True)
	raise Http404()

@login_required
@csrf_exempt
def unfollow(request):
	if request.method == "POST":
		usrname = request.POST.get('user')
		following = get_object_or_404(User, username = usrname)
		following.profile.followers.remove(request.user)
		request.user.profile.following.remove(following)
		return HttpResponse(True)
	raise Http404()


@login_required
def search(request):
	q = request.GET.get('q')
	if q:
		users = User.objects.filter(
		Q(username__icontains = q) |
		Q(first_name__icontains = q) |
		Q(last_name__icontains = q)
		).distinct()
	else:
		users = request.user.profile.non_followed_user
	return render(request, 'main/search.html', {'users': users})


@login_required
@csrf_exempt
def add_comment(request):
	if request.method =="POST":
		post_id = request.POST.get('post_id')
		comm = request.POST.get('comm')
		obj = Comment.objects.create(user=request.user, 
			post = Post.objects.get(id=int(post_id)),
			comm = comm,
			)
		return JsonResponse({
			'url': request.user.profile.profile_pic.url,
			'name': f"{request.user.first_name} {request.user.last_name}",
			'text': obj.comm,
			'id': obj.id,
			})
	raise Http404()

@login_required
@csrf_exempt
def add_subcomment(request):
	if request.method =="POST":
		comm_id = request.POST.get('comm_id')
		comm = request.POST.get('comm')
		obj = SubComment.objects.create(user=request.user, 
			comment = Comment.objects.get(id=int(comm_id)),
			comm = comm,
			)
		return JsonResponse({
			'url': request.user.profile.profile_pic.url,
			'name': f"{request.user.first_name} {request.user.last_name}",
			'text': obj.comm,
			'id': obj.id,
			})
	raise Http404()