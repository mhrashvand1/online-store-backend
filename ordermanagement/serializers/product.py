from rest_framework import serializers
from product.models import Product
from django.urls import reverse
from common.utils import get_abs_url


class ProductSerializer(serializers.ModelSerializer):
    
    url = serializers.SerializerMethodField()
    discounted_price = serializers.ReadOnlyField(source='get_discounted_price')
    discount_amount = serializers.ReadOnlyField(source='get_discount_amount')
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 
            'price', 'discount_percent', 'discounted_price', 'discount_amount',
            'url',
        ]

    def get_url(self, obj):
        url = reverse("product:products-detail", kwargs={"slug":obj.slug})
        return get_abs_url(url)
