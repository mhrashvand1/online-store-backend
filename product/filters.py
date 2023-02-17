from django_filters import rest_framework as filters
from product.models import Category, Product


class CategoryFilter(filters.FilterSet):
    product_count = filters.DateTimeFilter(field_name='product_count')
    product_count__lt = filters.DateTimeFilter(field_name='product_count', lookup_expr='lt')
    product_count__gt = filters.DateTimeFilter(field_name='product_count', lookup_expr='gt')

    class Meta:
        model = Category
        fields = []
        

class ProductFilter(filters.FilterSet):
    price__lt = filters.DateTimeFilter(field_name='price', lookup_expr='lt')
    price__gt = filters.DateTimeFilter(field_name='price', lookup_expr='gt')
    stock__lt = filters.DateTimeFilter(field_name='stock', lookup_expr='lt')
    stock__gt = filters.DateTimeFilter(field_name='stock', lookup_expr='gt') 
    
    class Meta:
        model = Product
        fields = ['price', 'category', 'stock',]