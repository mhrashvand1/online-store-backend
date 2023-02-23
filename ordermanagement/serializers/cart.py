from rest_framework import serializers
from ordermanagement.models import Cart, CartItem
from product.models import Product
from rest_framework.exceptions import ValidationError
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from ordermanagement.serializers.product import ProductSerializer



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
    postage_fee = serializers.ReadOnlyField(source='get_postage_fee')
    final_price = serializers.ReadOnlyField(source='get_final_price')
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items_count',
            'total_price', 'total_discounted_price', 'total_discount',
            'postage_fee', 'final_price', 'items'
        ]
     
##############################################################
##############################################################
##############################################################   
        
class CartAddProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(required=True, allow_null=False)

    def validate(self, data):
        product_id = data['product_id']
        
        product_qs = Product.objects.filter(id=data['product_id'])
        if not product_qs.exists():
            raise ValidationError(f"There is no product with ID {product_id}")
        
        product = product_qs.first()
        request = self.context['request']
        data['product'] = product
        
        if request.user.is_authenticated:
            return self._authenticated_validate(data, request, product)
        else:
            return self._anonymous_validate(data, request, product)
    
    
    def _authenticated_validate(self, data, request, product):
        stock = product.stock
        cart = request.user.cart
        
        cart_item_qs = cart.items.filter(product=product)
        if cart_item_qs.exists():
            item = cart_item_qs.first()
            item_quantity = item.quantity
            
            if item_quantity + 1 > settings.MAX_ITEM_QUANTITY:
                raise ValidationError(f"The maximum quantity of products in each item is {settings.MAX_ITEM_QUANTITY}")
            
            if item_quantity + 1 > stock:
                raise ValidationError(f"The product stock is {stock}")
            
            data['is_new_item'] = False
            data['item'] = item
        
        else:
            if not stock > 0:
                raise ValidationError("The product stock is 0")
            
            if not cart.items.aggregate(count=Count('id'))['count'] < settings.MAX_CART_ITEMS:
                raise ValidationError(f"The Item count limit is {settings.MAX_CART_ITEMS}.")      
        
            data['is_new_item'] = True
            
        return data
    
    
    def _anonymous_validate(self, data, request, product):
        stock = product.stock
        cart = request.session.get('cart', {})
        product_id = str(data['product_id'])
        
        if cart.get(product_id):
            item_quantity = cart[product_id]
            if item_quantity + 1 > settings.MAX_ITEM_QUANTITY:
                raise ValidationError(f"The maximum quantity of products in each item is {settings.MAX_ITEM_QUANTITY}")
            
            if item_quantity + 1 > stock:
                raise ValidationError(f"The product stock is {stock}") 
            
            data['is_new_item'] = False
        
        else:
            if not stock > 0:
                raise ValidationError("The product stock is 0")
            
            if not len(cart) < settings.MAX_CART_ITEMS:
                raise ValidationError(f"The Item count limit is {settings.MAX_CART_ITEMS}.")
            
            data['is_new_item'] = True 

        return data
    
    
    def perform_add_product(self):
        request = self.context['request']
        product = self.validated_data['product']
        product_id = str(self.validated_data['product_id'])
        is_new_item = self.validated_data['is_new_item']
        
        if request.user.is_authenticated:
            cart = request.user.cart
            if is_new_item:
                CartItem.objects.create(cart=cart, product=product)
            else:
                item = self.validated_data['item']
                item.quantity += 1
                item.save()
        else:
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + 1
            cart_expiration_time = timezone.now() + timedelta(days=settings.ANONYMOUS_CART_EXPIRATION)
            request.session['cart'] = cart
            request.session.set_expiry(cart_expiration_time)
        
##########################################################################
##########################################################################
##########################################################################

class CartSubtractProductSerialzier(serializers.Serializer):
    product_id = serializers.UUIDField(required=True, allow_null=False)

    def validate(self, data):          
        request = self.context['request']     
        if request.user.is_authenticated:
            return self._authenticated_validate(data, request)
        else:
            return self._anonymous_validate(data, request)
    
    def _authenticated_validate(self, data, request):
        product_id = data['product_id']
        cart = request.user.cart
        
        cart_items_qs = cart.items.filter(product_id=product_id)
        if not cart_items_qs.exists():
            raise ValidationError(
                f"Item with product {product_id} does not exists."
            )
        
        data['item'] = cart_items_qs.first() 
        return data
    
    
    def _anonymous_validate(self, data, request):
        product_id = str(data['product_id'])
        cart = request.session.get('cart', {})

        if not cart.get(product_id):
            raise ValidationError(f"Item with product {product_id} does not exists.")
        
        return data    
    
    
    def perform_subtract_product(self):
        request = self.context['request']
        
        if request.user.is_authenticated:
            item = self.validated_data['item']
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
                
        else:
            product_id = str(self.validated_data['product_id'])
            cart = request.session.get('cart', {})

            if cart[product_id] > 1:
                cart[product_id] -= 1
            else:
                del cart[product_id]
                
            cart_expiration_time = timezone.now() + timedelta(days=settings.ANONYMOUS_CART_EXPIRATION)
            request.session['cart'] = cart
            request.session.set_expiry(cart_expiration_time)
            
       