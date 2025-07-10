from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .SignUpForm import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile
from .LoginForm import LoginForm



# def login_view(request):
    # if request.method == 'POST':
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             messages.success(request, 'Login successful!')
    #             return redirect('profile')  # Redirect to profile page after login') 
    #         else:
    #             messages.error(request, 'Invalid credentials.')
    # else:
    #     form = LoginForm()
    # return render(request, 'accounts/login.html', {'form': form})

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
            return redirect('login')
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
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'profile/change_password.html', {
        'form': form
    })


from django.http import JsonResponse
def upload_profile_picture(request):
    """Handle profile picture upload via AJAX"""
    if request.method == 'POST':
        try:
            if 'profile_picture' not in request.FILES:
                return JsonResponse({'success': False, 'error': 'No file uploaded'})
            
            file = request.FILES['profile_picture']
            
            # Validate file size (max 5MB)
            if file.size > 5 * 1024 * 1024:
                return JsonResponse({'success': False, 'error': 'File too large. Maximum size is 5MB.'})
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if file.content_type not in allowed_types:
                return JsonResponse({'success': False, 'error': 'Invalid file type. Only JPEG, PNG, GIF, and WebP are allowed.'})
            
            # Get or create profile
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Delete old profile picture if it exists
            if profile.profile_picture:
                if default_storage.exists(profile.profile_picture.name):
                    default_storage.delete(profile.profile_picture.name)
            
            # Save new profile picture
            profile.profile_picture = file
            profile.save()
            
            return JsonResponse({
                'success': True,
                'image_url': profile.profile_picture.url,
                'message': 'Profile picture updated successfully!'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def logout_view(request):
    """Handle user logout"""
    auth.logout(request)  # ✅ correct logout function
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login')  