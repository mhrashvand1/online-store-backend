from django.urls import path, re_path, include
from rest_framework.routers import SimpleRouter
from product.views import CategoryViewSet, ProductViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('products', ProductViewSet, basename='products')

app_name = 'product'
urlpatterns = [
]
urlpatterns += router.urls