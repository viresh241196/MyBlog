from django.shortcuts import render, redirect
from .form import UserRegisterForm, ProfileRegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User, auth


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            new_profile = Profile.objects.create(user_id=user.id)
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} your account has been created! You will be able to login now')
            return redirect('blog-home')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('blog-home')
        else:
            messages.warning(request, "invalid credentials")
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout(request):
    auth.logout(request)
    return redirect('blog-home')


def profileupdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Changes has been applied")
            return redirect('profile')
        else:
            messages.success(request, f"error")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', {'p_form': p_form, 'u_form': u_form})
