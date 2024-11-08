from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, LoginForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
            else:
                user = form.save()
                messages.success(request, 'Registration successful.')
                # return redirect('index')
        else:
            messages.error(request, 'An error occurred during registration.')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return render (request, 'index.html')


# def profile(request):
#     return render(request, 'auth/profile.html')



@login_required
def edit_profile(request):
    user_profile = request.user.userprofile
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user_profile, user=request.user)
    
    return render(request, 'auth/edit_profile.html', {'form': form})