from django_filters import rest_framework as filters
from wallet.models import Wallet, Payment


class WalletFilter(filters.FilterSet):
    balance__lt = filters.NumberFilter(field_name='balance', lookup_expr='lt')
    balance__gt = filters.NumberFilter(field_name='balance', lookup_expr='gt')
    user = filters.CharFilter(field_name='user', lookup_expr='phone_number')

    class Meta:
        model = Wallet
        fields = ['balance',]
        

class PaymentFilter(filters.FilterSet):
    amount__lt = filters.NumberFilter(field_name='amount', lookup_expr='lt')
    amount__gt = filters.NumberFilter(field_name='amount', lookup_expr='gt')
    user = filters.CharFilter(field_name='user', lookup_expr='phone_number')

    class Meta:
        mdoel = Payment
        fields = ['status', 'error_code', 'amount']