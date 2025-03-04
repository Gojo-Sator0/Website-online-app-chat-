from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from accounts.models import User
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
           username = request.POST['username']
           password = request.POST['password']
           user = auth.authenticate(username=username, password=password)
           if user:
               auth.login(request, user)
               return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()
        
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
        
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.user == profile_user:
        if request.method == 'POST':
            form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:profile', args=[request.user.username]))
        else:
            form = UserProfileForm(instance=request.user)
    else:
        form = None  # Другие пользователи не могут редактировать чужие профили

    context = {
        'profile_user': profile_user,
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def logout_view(request):
    auth.logout(request)
    return redirect(reverse('main:index'))