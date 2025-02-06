from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from accounts.forms import UserLoginForm, UserRegistrationForm
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
            user = form.isinstance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
        
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def profile_view(request):
    return render(request, 'accounts/profile.html')

def logout_view(request):
    auth.logout(request)
    return redirect(reverse('main:index'))