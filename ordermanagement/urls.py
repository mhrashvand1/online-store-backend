from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter
from ordermanagement import views


router = SimpleRouter()
app_name = 'ordermanagement'
urlpatterns = [
    
]
urlpatterns += router.urls
