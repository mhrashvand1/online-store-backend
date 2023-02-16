from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework.routers import SimpleRouter
from account import views

router = SimpleRouter()
router.register("users", views.UserViewSet, basename="users") 

app_name = 'account'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('auth/confirm/', views.AuthConfirmView.as_view(), name='auth_confirm'),
    path(
        'profile/',
        views.ProfileViewSet.as_view({
            'get':'retrieve',
            'put':'update',
            'patch':'partial_update',
        })
    ),
    path('location/', views.GetLocationView.as_view(), name='location'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
]
urlpatterns += router.urls