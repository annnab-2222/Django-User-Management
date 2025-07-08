from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .SignUpForm import SignUpForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False 
            user.save()
            login(request, user)
            # Send verification email here (mock or real)
            print(f"Verification link for user {user.username} sent!")  # Mock
            return redirect('verification_sent')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# @login_required
def edit_profile(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = SignUpForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

