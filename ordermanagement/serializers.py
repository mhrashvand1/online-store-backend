from rest_framework import serializers
from ordermanagement.models import Cart, CartItem, Order, OrderItem
from product.models import Product
from django.urls import reverse
from common.utils import get_abs_url
from account.serializers import UserReadOnlySerializer


class ProductSerializer(serializers.ModelSerializer):
    
    url = serializers.SerializerMethodField()
    discounted_price = serializers.ReadOnlyField(source='get_discounted_price')
    discount_amount = serializers.ReadOnlyField(source='get_discount_amount')
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 
            'price', 'discount_percent', 'discounted_price', 
            'url',
        ]

    def get_url(self, obj):
        url = reverse("product:products-detail", kwargs={"slug":obj.slug})
        return get_abs_url(url)


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    item_price = serializers.ReadOnlyField(source='get_item_price')
    item_discounted_price = serializers.ReadOnlyField(source='get_item_discounted_price')
    item_discount_amount =  serializers.ReadOnlyField(source='get_item_discount_amount')
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'cart', 
            'item_price', 'item_discounted_price', 'item_discount_amount',
            'product', 'quantity'
        ]
    
        
class CartSerializer(serializers.ModelSerializer):
    # user = UserReadOnlySerializer()
    items_count = serializers.ReadOnlyField(source='get_items_count')
    total_price = serializers.ReadOnlyField(source='get_total_price')
    total_discounted_price = serializers.ReadOnlyField(source='get_total_discounted_price')
    total_discount = serializers.ReadOnlyField(source='get_total_discount')
    postage_fee = serializers.ReadOnlyField(sourec='get_postage_fee')
    final_price = serializers.ReadOnlyField(source='get_final_price')
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items_count',
            'total_price', 'total_discounted_price', 'total_discount',
            'postage_fee', 'final_price', 'items'
        ]