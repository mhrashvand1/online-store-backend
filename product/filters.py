from django_filters import rest_framework as filters
from product.models import Category, Product


class CategoryFilter(filters.FilterSet):
    product_count = filters.NumberFilter(field_name='product_count')
    product_count__lt = filters.NumberFilter(field_name='product_count', lookup_expr='lt')
    product_count__gt = filters.NumberFilter(field_name='product_count', lookup_expr='gt')

    sales_count = filters.NumberFilter(field_name='sales_count')
    sales_count__lt = filters.NumberFilter(field_name='sales_count', lookup_expr='lt')
    sales_count__gt = filters.NumberFilter(field_name='sales_count', lookup_expr='gt')

    last_week_sales_count = filters.NumberFilter(field_name='last_week_sales_count')
    last_week_sales_count__lt = filters.NumberFilter(field_name='last_week_sales_count', lookup_expr='lt')
    last_week_sales_count__gt = filters.NumberFilter(field_name='last_week_sales_count', lookup_expr='gt')

    class Meta:
        model = Category
        fields = []
        

class ProductFilter(filters.FilterSet):
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    
    stock__lt = filters.NumberFilter(field_name='stock', lookup_expr='lt')
    stock__gt = filters.NumberFilter(field_name='stock', lookup_expr='gt') 
    
    discount_percent__lt = filters.NumberFilter(field_name='discount_percent', lookup_expr='lt')
    discount_percent__gt = filters.NumberFilter(field_name='discount_percent', lookup_expr='gt')

    discounted_price = filters.NumberFilter(field_name='discounted_price')
    discounted_price__lt = filters.NumberFilter(field_name='discounted_price', lookup_expr='lt')
    discounted_price__gt = filters.NumberFilter(field_name='discounted_price', lookup_expr='gt')

    discount_amount = filters.NumberFilter(field_name='discount_amount')
    discount_amount__lt = filters.NumberFilter(field_name='discount_amount', lookup_expr='lt')
    discount_amount__gt = filters.NumberFilter(field_name='discount_amount', lookup_expr='gt')

    sales_count = filters.NumberFilter(field_name='sales_count')
    sales_count__lt = filters.NumberFilter(field_name='sales_count', lookup_expr='lt')
    sales_count__gt = filters.NumberFilter(field_name='sales_count', lookup_expr='gt')

    last_week_sales_count = filters.NumberFilter(field_name='last_week_sales_count')
    last_week_sales_count__lt = filters.NumberFilter(field_name='last_week_sales_count', lookup_expr='lt')
    last_week_sales_count__gt = filters.NumberFilter(field_name='last_week_sales_count', lookup_expr='gt')

    class Meta:
        model = Product
        fields = ['price', 'category', 'stock', 'discount_percent',]