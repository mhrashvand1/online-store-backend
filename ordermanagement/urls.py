from django.urls import path
from rest_framework.routers import SimpleRouter
from ordermanagement import views


router = SimpleRouter()
router.register('carts', views.CartViewSet, basename='carts')
router.register('orders', views.OrderViewSet, basename='orders')
app_name = 'ordermanagement'
urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path(
        'orders/deleted_orders_detail/<str:pk>/',
        views.OrderViewSet.as_view({"get":"deleted_orders_detail"}),
        name="orders-deleted_orders_detail"
    )
]
router_urls = router.urls
urlpatterns += [url for url in router_urls if url.name != 'orders-deleted_orders_detail']
