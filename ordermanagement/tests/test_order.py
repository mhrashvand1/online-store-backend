from ordermanagement.tests.base_test import BaseTest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account.models import User
from ordermanagement.models import Order, OrderItem
from django.conf import settings


class Test(BaseTest):
    
    def test_cart_model(self):
        order = Order.objects.create(
            user=self.user1, status='paid', postage_fee=12000
        )
        item1 = OrderItem.objects.create(
            order=order,
            product=self.product1, 
            quantity=1,
            p_id=self.product1.id,
            p_name=self.product1.name,
            p_price=self.product1.price,
            p_discount_percent=10 # changed
        )
        item2 = OrderItem.objects.create(
            order=order,
            product=self.product2, 
            quantity=2,
            p_id=self.product2.id,
            p_name=self.product2.name,
            p_price=self.product2.price,
            p_discount_percent=10 # changed
        )
        item3 = OrderItem.objects.create(
            order=order,
            product=self.product3, 
            quantity=3,
            p_id=self.product3.id,
            p_name=self.product3.name,
            p_price=self.product3.price,
            p_discount_percent=10 # changed
        )
        
        self.assertEqual(order.get_items_count(), 3)
        self.assertEqual(order.get_total_price(), 120000) # 1*20000 + 2*20000 + 3*20000
        self.assertEqual(order.get_total_discounted_price(), 108000) # 120000 - 120000 * 10%
        self.assertEqual(order.get_total_discount(), 12000) # 120000 * 10%
        self.assertEqual(order.get_final_price(), 108000 + 12000) # add postage fee
        
        self.assertEqual(item3.get_item_price(), 60000)
        self.assertEqual(item3.get_item_discounted_price(), 54000)
        self.assertEqual(item3.get_item_discount_amount(), 6000)
    