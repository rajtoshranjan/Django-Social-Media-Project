from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			name = form.cleaned_data.get('name').split(' ')

			usr = User.objects.get(username=username)
			usr.email = username
			usr.first_name = name[0]
			usr.last_name = name[1]
			usr.save()
			messages.success(request, f'Account is Created For {username}')
			return redirect('login')
	else:
		form = SignUpForm()

	return render(request, 'user/signup.html', {'form':form})



