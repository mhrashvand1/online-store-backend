from rest_framework import serializers
from ordermanagement.models import Order, OrderItem
from rest_framework.exceptions import ValidationError
from django.db import transaction
from rest_framework.exceptions import APIException
from ordermanagement.serializers.product import ProductSerializer



class CheckoutSerializer(serializers.Serializer):
    
    def validate(self, data):
        cart = self.context['cart']
        user_wallet = self.context['user_wallet']
        
        cart_items = cart.items.all()
        
        # Check if user added product to the cart
        if not cart_items.exists():
            raise ValidationError("You cart is empty.")
        
        # Check user wallet amount
        if user_wallet.balance < cart.get_final_price():
            raise ValidationError("Your wallet balance is not enough")
        
        # Check product stock
        for item in cart_items:
            product = item.product
            product_stock = product.stock
            item_quantity = item.quantity
            item_id = item.id
            if item_quantity > product_stock:
                error_msg = {
                    "detail":f"The quantity of item {item_id} is more than the product stock.",
                    "item_id":item_id,
                    "item_quantity":item_quantity,
                    "product":ProductSerializer(
                        product,
                        context=self.context['view'].get_serializer_context()
                    ).data
                }
                error_msg['product']['stock'] = product_stock
                raise ValidationError(error_msg)
        
        data['cart_items'] = cart_items
        return data
    
    
    def perform_checkout(self):
        cart = self.context['cart']
        user_wallet = self.context['user_wallet']
        user = self.context['request'].user
        cart_items = self.validated_data['cart_items']
        
        try:
            with transaction.atomic():       
                # 1 Creating the order and its items and reducing the product stock
                order = Order.objects.create(
                    user=user, postage_fee=cart.get_postage_fee()
                )
                for item in cart_items:
                    product = item.product
                    quantity = item.quantity
                    product_id = product.id
                    product_name = product.name
                    product_price = product.price
                    product_discount_percent = product.discount_percent
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        p_id=product_id,
                        p_name=product_name,
                        p_price=product_price,
                        p_discount_percent=product_discount_percent
                    )
                    # Reduce product stock
                    product.stock -= quantity
                    product.save()
                    
                # 2 Deducting the final price from the user's wallet
                user_wallet.balance -= order.get_final_price()
                user_wallet.save()
                
                # 3 Remove cart items
                cart_items.delete()
                
        except:
            raise APIException("Error while checkout.")
        
        return order