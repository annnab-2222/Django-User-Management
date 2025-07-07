from django.shortcuts import render, redirect
from django.contrib.auth import login
from .SignUpForm import SignUpForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Ensure 'profile' is a named URL
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
