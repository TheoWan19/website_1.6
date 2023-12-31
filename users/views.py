from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . forms import UserRegistrationForm, UserLoginForm, UserUpdateForm
from . decorators import user_not_authenticated
from . models import CustomUser, Profile

# Create your views here.
@user_not_authenticated
def register(request):
	if request.user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, f'New account created for {user.username}')
			return redirect('home')
		else:
			for error in list(form.errors.values()):
				messages.error(request, error)
	else:
		form = UserRegistrationForm()

	return render(request, 'users/register.html', context={'form': form})	

@login_required
def custom_logout(request):
	logout(request)
	messages.info(request, 'Logged out successfully!')
	return redirect('home')	


@user_not_authenticated
def custom_login(request):
	
	if request.method == 'POST':
		form = UserLoginForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(
					username = form.cleaned_data.get('username'),
					password = form.cleaned_data.get('password'),
			)
			if user is not None:
				login(request, user)
				print(user)
				messages.success(request, f'Hello <strong>{user.username}</strong>! You have been logged in.')
				return redirect('home')
		else:
			for key, error in list(form.errors.items()):
				if key == 'captcha' and error[0] == 'This field is required.':
					messages.error(request, 'You must pass the reCAPTCHA test')
					continue
				messages.error(request, error)		

	form = UserLoginForm()
	
	return render(
		request=request, 
		template_name='users/login.html', 
		context={'form': form})

def profile_list(request):
	if request.user.is_authenticated:
		profiles = Profile.objects.exclude(user=request.user)
		return render(request, 'users/profile_list.html', {'profiles': profiles})	
	else:
		messages.info(request, ("You must be logged in to view this page!"))	
		return redirect('home')


def profile(request, username):
	if request.method == 'POST':
		user = request.user
		form = UserUpdateForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			user_form = form.save()	
			messages.success(request, f'{user_form.username}, Your profile has been updated!')
			return redirect('profile', user_form.username)

		for error in list(form.errors.values()):
				messages.error(request, error)	

	user = CustomUser.objects.filter(username=username).first()
	if user:
		form = UserUpdateForm(instance=user)
		return render(
			request=request, 
			template_name='users/profile.html',
			context={'form':form})
	return redirect('home')	
