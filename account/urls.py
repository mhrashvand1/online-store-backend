from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import SimpleRouter
from account import views

app_name = 'account'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('auth/confirm/', views.AuthConfirmView.as_view(), name='auth_confirm'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]