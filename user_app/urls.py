from django.urls import path, re_path, include
from user_app.views import UserRegisterView,UserLoginView,UpdateProfileView,UserLogoutView,UserProfileView, PasswordResetView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
]