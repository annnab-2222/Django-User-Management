from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
     path('profile/', views.profile, name='profile'),
     path('register/', views.register, name='register'),
     path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  
     path('admin/', admin.site.urls),
     # path('accounts/', include('accounts.urls')),

]


