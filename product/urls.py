from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter
from product.views import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='categories')

app_name = 'product'
urlpatterns = [
    
]
urlpatterns += router.urls