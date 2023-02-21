from ordermanagement.tests.base_test import BaseTest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from ordermanagement.models import Cart, CartItem
from config.settings import POSTAGE_FEE


class Test(BaseTest):
    
    def test_cart_model(self):
        user1_cartitem1 = CartItem.objects.create(
            cart=self.user1.cart,
            product=self.product1,
            quantity=1
        )
        user1_cartitem2 = CartItem.objects.create(
            cart=self.user1.cart,
            product=self.product2,
            quantity=2
        )
        user1_cartitem3 = CartItem.objects.create(
            cart=self.user1.cart,
            product=self.product3,
            quantity=3
        )
        
        user1_cart = self.user1.cart
        self.assertEqual(user1_cart.get_items_count(), 3)
        self.assertEqual(user1_cart.get_total_price(), 120000) # 1*20000 + 2*20000 + 3*20000
        self.assertEqual(user1_cart.get_total_discounted_price(), 96000) # 120000 - 120000 * 20%
        self.assertEqual(user1_cart.get_total_discount(), 24000) # 120000 * 20%
        self.assertEqual(user1_cart.get_final_price(), 96000 + POSTAGE_FEE)
        
        self.assertEqual(user1_cartitem3.get_item_price(), 60000)
        self.assertEqual(user1_cartitem3.get_item_discounted_price(), 48000)
        self.assertEqual(user1_cartitem3.get_item_discount_amount(), 12000)
    
    
    def test_addproduct_without_signin(self):
        # client_a = APIClient()
        # client_a.force_authenticate(user=self.user_a)
        # client_b = APIClient()
        # client_b.force_authenticate(user=self.user_b)
        pass