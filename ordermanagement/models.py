from django.db import models
from common.models import BaseModel, UUIDBaseModel
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ 
from django.db.models import Count, F, Sum
from config.settings import POSTAGE_FEE, MAX_ITEM_QUANTITY
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


############################################################################
############################    CART    ###################################
############################################################################

class Cart(UUIDBaseModel):
    
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='cart',
        db_index=True,
        verbose_name=_('user')
    )
    
    def __str__(self) -> str:
        return f"cart: {self.id} user: {self.user.phone_number}"
    
    def get_items_count(self):
        return self.items.aggregate(Count("id"))["id__count"]
    
    def get_total_price(self):
        total_price = self.items.aggregate(
            x=Sum(
                F("quantity")*F('product__price')
            )
        )
        return total_price['x']

    def get_total_discounted_price(self):
        total_discounted_price = self.items.aggregate(
            x = Sum(
                F("quantity")*(F('product__price') - F('product__price')*F('product__discount_percent')/100)
            )
        )
        return total_discounted_price['x']
        
    
    def get_total_discount(self):
        total_discount = self.items.aggregate(
            x=Sum(
                F("quantity")*
                (
                    F("product__price")*F("product__discount_percent")/100
                )
            )
        )
        return total_discount['x']
    
    def get_final_price(self):
        return self.get_total_discounted_price() + POSTAGE_FEE
           
    class Meta:
        db_table = 'Cart'
        verbose_name = _('cart')
        verbose_name_plural = _('cart')
        
        
class CartItem(UUIDBaseModel):
    
    cart = models.ForeignKey(
        to='Cart',
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
        verbose_name=_('cart')
    )
    product = models.ForeignKey(
        to='product.Product',
        on_delete=models.CASCADE,
        related_name='cartitems',
        verbose_name=_('product')
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=(MinValueValidator(1), MaxValueValidator(MAX_ITEM_QUANTITY))
    )
    
    def __str__(self) -> str:
        return f"cartitem: {self.id} user: {self.cart.user.phone_number}"
    
    def get_item_price(self):
        return self.quantity * self.product.price 
    
    def get_item_discounted_price(self):
        return self.quantity * self.product.get_discounted_price()
  
    def get_item_discount_amount(self):
        return self.quantity * self.product.get_discount_amount()

    class Meta:
        db_table = 'CartItem'
        verbose_name = _('cartitem')
        verbose_name_plural = _('cartitems')
        unique_together = [('cart', 'product'),]
  
############################################################################      
############################################################################
############################    ORDER    ###################################
############################################################################
############################################################################

class ActiveOrderManager(models.Manager):    
    def get_queryset(self):
        return super().get_queryset().exclude(status='deleted')

class Order(UUIDBaseModel):
    
    objects = ActiveOrderManager()  
    all_objects = models.Manager()  
    
    order_status = [
        ('paid', 'paid'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('deleted', 'deleted')
    ]
    
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='orders',
        db_index=True,
        verbose_name=_('user')
    )
    status = models.CharField(max_length=20, choices=order_status, default='paid')
    postage_fee = models.BigIntegerField()
        
    def __str__(self) -> str:
        return f"{self.id}-user: {self.user.phone_number}-status: {self.status}"
     
    def delete(self, hard=False, *args, **kwargs):
        if hard:
            return super().delete(*args, **kwargs)
        else:
            self.status = 'deleted'
            self.save()

    def get_items_count(self):
        return self.items.aggregate(Count("id"))["id__count"]

    def get_total_price(self):
        total_price = self.items.aggregate(
            x=Sum(
                F("quantity")*F('p_price')
            )
        )
        return total_price['x']
        
    def get_total_discounted_price(self):
        total_discounted_price = self.items.aggregate(
            x = Sum(
                F("quantity")*(F('p_price') - F('p_price')*F('p_discount_percent')/100)
            )
        )
        return total_discounted_price['x']
    
    def get_total_discount(self):
        total_discount = self.items.aggregate(
            x=Sum(
                F("quantity")*
                (
                    F("p_price")*F("p_discount_percent")/100
                )
            )
        )
        return total_discount['x']
    
    def get_final_price(self):
        return self.get_total_discounted_price() + self.postage_fee
    
    class Meta:
        db_table = 'Order'
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class OrderItem(UUIDBaseModel):
    order = models.ForeignKey(
        to='Order',
        on_delete=models.PROTECT,
        related_name='items',
        db_index=True,
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        to='product.Product',
        on_delete=models.SET_NULL,
        related_name='orderitems',
        null=True,
        verbose_name=_('product')
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        validators=(MinValueValidator(1), MaxValueValidator(MAX_ITEM_QUANTITY))
    )
    # To display invoices in case of product removal or changes in product price, ...
    # We need to store sensitive product data directly in the Order table
    p_id = models.UUIDField(
        verbose_name=_("product id")
    )
    p_name = models.CharField(
        max_length=255,
        verbose_name=_('product name')
    )
    p_price = models.PositiveBigIntegerField(
        verbose_name=_('product price')
    )
    p_discount_percent = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0, 
        verbose_name=_('product discount percent')
    )

    def __str__(self) -> str:
        return super().__str__()

    def get_item_price(self):
        return self.quantity * self.p_price
    
    def get_item_discounted_price(self):
        result = self.quantity * (
            self.p_price - 
            self.p_price*(self.p_discount_percent/100)
        )
        return result
  
    def get_item_discount_amount(self):
        result = self.quantity * (
            self.p_price*(self.p_discount_percent/100)
        )
        return result    
    
    class Meta:
        db_table = 'OrderItem'
        verbose_name = _('orderitem')
        verbose_name_plural = _('orderitems')
        unique_together = [('order', 'product'),]