from django.urls import path
from users import views as users_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', users_views.register, name='register'),
    path('activate/<uidb64>/<token>', users_views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', users_views.profile, name='profile'),
    path('profile/<str:username>/view/', users_views.ProfileView.as_view(), name='profile-view')
]
