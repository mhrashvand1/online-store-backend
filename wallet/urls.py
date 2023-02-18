from django.urls import path, include
from rest_framework.routers import SimpleRouter
from wallet import views

router = SimpleRouter()
router.register('wallets', views.WalletViewSet, basename='wallets')
router.register('payments', views.PaymentViewSet, basename='payments')

app_name = 'wallet'
urlpatterns = [
    path(
        'fakechargewallet/', 
        views.FakeChargeWalletView.as_view(),
        name='fake-chargewallet'
    ),
]
urlpatterns += router.urls