from django.urls import path, include
from rest_framework.routers import SimpleRouter
from wallet import views

router = SimpleRouter()

app_name = 'wallet'
urlpatterns = [
    
]
urlpatterns += router.urls