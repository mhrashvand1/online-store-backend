from django_filters import rest_framework as filters
from ordermanagement.models import Order


class OrderFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user', lookup_expr='phone_number')
    
    postage_fee__lt = filters.NumberFilter(field_name='postage_fee', lookup_expr='lt')
    postage_fee__gt = filters.NumberFilter(field_name='postage_fee', lookup_expr='gt')

    items_count = filters.NumberFilter(field_name='items_count')
    items_count__lt = filters.NumberFilter(field_name='items_count', lookup_expr='lt')
    items_count__gt = filters.NumberFilter(field_name='items_count', lookup_expr='gt')
    
    total_price = filters.NumberFilter(field_name='total_price')
    total_price__lt = filters.NumberFilter(field_name='total_price', lookup_expr='lt')
    total_price__gt = filters.NumberFilter(field_name='total_price', lookup_expr='gt')   
    
    total_discounted_price = filters.NumberFilter(field_name='total_discounted_price')
    total_discounted_price__lt = filters.NumberFilter(field_name='total_discounted_price', lookup_expr='lt')
    total_discounted_price__gt = filters.NumberFilter(field_name='total_discounted_price', lookup_expr='gt')    
    
    total_discount = filters.NumberFilter(field_name='total_discount')
    total_discount__lt = filters.NumberFilter(field_name='total_discount', lookup_expr='lt')
    total_discount__gt = filters.NumberFilter(field_name='total_discount', lookup_expr='gt')    
    
    final_price = filters.NumberFilter(field_name='final_price')
    final_price__lt = filters.NumberFilter(field_name='final_price', lookup_expr='lt')
    final_price__gt = filters.NumberFilter(field_name='final_price', lookup_expr='gt')
    
    class Meta:
        model = Order
        fields = ['status', 'postage_fee']
        
        