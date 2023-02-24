from rest_framework import serializers
from ordermanagement.models import Order, OrderItem
from django.urls import reverse
from common.utils import get_abs_url
from account.serializers import UserReadOnlySerializer

       
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    item_price = serializers.ReadOnlyField(source='get_item_price')
    item_discounted_price = serializers.ReadOnlyField(source='get_item_discounted_price')
    item_discount_amount =  serializers.ReadOnlyField(source='get_item_discount_amount')
    
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 
            'item_price', 'item_discounted_price', 'item_discount_amount',
            'product', 'quantity', 'created_at', 'updated_at',
        ]
    
    def get_product(self, obj):
        result = {
            "id":str(obj.p_id),
            "name":obj.p_name,
            "price":obj.p_price,
            "discount_percent":obj.p_discount_percent,
            "discounted_price":0,
            "discount_amount":0,
            # The only field related to the product object is url
            "url":None
        }
        result['discounted_price'] = result['price'] - result['price']*result['discount_percent']/100
        result['discount_amount'] = result['price'] - result['discounted_price']
        
        product_obj = obj.product
        if product_obj:
            result['url'] = get_abs_url(
                reverse(
                    'product:products-detail', 
                    kwargs={"slug":product_obj.slug}
                )
            )
        
        return result
            

class OrderSerializer(serializers.ModelSerializer):
    user = UserReadOnlySerializer()
    items_count = serializers.ReadOnlyField(source='get_items_count')
    total_price = serializers.ReadOnlyField(source='get_total_price')
    total_discounted_price = serializers.ReadOnlyField(source='get_total_discounted_price')
    total_discount = serializers.ReadOnlyField(source='get_total_discount')
    final_price = serializers.ReadOnlyField(source='get_final_price')
    items = OrderItemSerializer(many=True)
    detail = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'status', 'user', 
            'items_count',
            'total_price', 'total_discounted_price', 'total_discount',
            'postage_fee', 'final_price', 'items', 'detail', 'created_at', 'updated_at'
        ] 
        
    def get_detail(self, obj):
        if obj.status == 'deleted':
            url = reverse(
                "ordermanagement:orders-deleted_orders_detail",
                kwargs={"pk":obj.pk}
            )
        else:
            url = reverse("ordermanagement:orders-detail", kwargs={"pk":obj.pk})
            
        return get_abs_url(url)
            


class OrderChangeStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        required=True, 
        allow_null=False,
        allow_blank=False,
        choices=[]
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user
        # Only superusers can return the product status to paid.
        if user.is_superuser:
            self.fields['status'].choices = ['paid', 'shipped', 'delivered']
        else:
            self.fields['status'].choices = ['shipped', 'delivered']
            
        super().__init__(*args, **kwargs)
        
      