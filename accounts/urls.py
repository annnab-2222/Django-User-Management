from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
     path('profile/', views.profile, name='profile'),
     # path('profile/edit/', views.edit_profile, name='edit_profile'),
     path('register/', views.register, name='register'),
     path('verify/<int:user_id>/', views.verify_user, name='verify_user'),
     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
     path('admin/', admin.site.urls),
     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
     path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

     # path('accounts/', include('accounts.urls')),
]



