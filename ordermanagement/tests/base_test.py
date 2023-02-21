from rest_framework.test import APITestCase
from account.models import User, Address, Location
from wallet.models import Wallet
from ordermanagement.models import Cart
from rest_framework.test import APIClient
from product.models import Category, Product


class BaseTest(APITestCase):
    def setUp(self):
        # Create superuser
        u = User.objects.create(
            phone_number="09035004342", 
            first_name='mmd', 
            last_name='rashvand',    
        )
        u.set_password("1234")
        u.is_superuser = True
        u.is_staff = True
        u.save()
        Address.objects.get_or_create(user=u)
        Location.objects.get_or_create(user=u)
        Wallet.objects.create(user=u, balance=0)
        Cart.objects.create(user=u)
        self.superuser = u
        
        # Create Admin User
        u = User.objects.create(
            phone_number="09197002020", 
            first_name='saman', 
            last_name='allaei',    
        )
        u.set_password("1234")
        u.is_staff = True
        u.save()
        Address.objects.get_or_create(user=u)
        Location.objects.get_or_create(user=u)
        Wallet.objects.create(user=u, balance=0)
        Cart.objects.create(user=u)
        self.adminuser = u
          
        # Create common user 1
        u = User.objects.create(
            phone_number="09124004040", 
            first_name='user1', 
            last_name='user1',    
        )
        u.set_password("1234")
        u.save()
        Address.objects.get_or_create(user=u)
        Location.objects.get_or_create(user=u)
        Wallet.objects.create(user=u, balance=0)
        Cart.objects.create(user=u)
        self.user1 = u   
        
        # Create common user 2
        u = User.objects.create(
            phone_number="09371111111", 
            first_name='user2', 
            last_name='user2',    
        )
        u.set_password("1234")
        u.save()
        Address.objects.get_or_create(user=u)
        Location.objects.get_or_create(user=u)
        Wallet.objects.create(user=u, balance=0)
        Cart.objects.create(user=u)
        self.user2 = u  
        
        
        # Create 3 categories
        self.category1 = Category.objects.create(
            name='c1', slug='c1', description='c1'
        )
        self.category2 = Category.objects.create(
            name='c2', slug='c2', description='c2'
        )
        self.category3 = Category.objects.create(
            name='c3', slug='c3', description='c3'
        )
        
        # Create 9 product    
        self.product1 = Product.objects.create(
            name='p1', description='p1', slug='p1', 
            price=20000, discount_percent=20, 
            category=self.category1, stock=12,
            main_image='someimage.png'
        )
        self.product2 = Product.objects.create(
            name='p2', description='p2', slug='p2', 
            price=20000, discount_percent=20, 
            category=self.category1, stock=12,
            main_image='someimage.png'
        )
        self.product3 = Product.objects.create(
            name='p3', description='p3', slug='p3', 
            price=20000, discount_percent=20, 
            category=self.category1, stock=12,
            main_image='someimage.png'
        )
        self.product4 = Product.objects.create(
            name='p4', description='p4', slug='p4', 
            price=25000, discount_percent=20, 
            category=self.category2, stock=12,
            main_image='someimage.png'
        )
        self.product5 = Product.objects.create(
            name='p5', description='p5', slug='p5', 
            price=30000, discount_percent=10, 
            category=self.category2, stock=12,
            main_image='someimage.png'
        )
        self.product6 = Product.objects.create(
            name='p6', description='p6', slug='p6', 
            price=42000, discount_percent=0, 
            category=self.category2, stock=12,
            main_image='someimage.png'
        )
        self.product7 = Product.objects.create(
            name='p7', description='p7', slug='p7', 
            price=31000, discount_percent=45, 
            category=self.category3, stock=12,
            main_image='someimage.png'
        )
        self.product8 = Product.objects.create(
            name='p8', description='p8', slug='p8', 
            price=20000, discount_percent=0, 
            category=self.category3, stock=12,
            main_image='someimage.png'
        )
        self.product9 = Product.objects.create(
            name='p9', description='p9', slug='p9', 
            price=22500, discount_percent=20, 
            category=self.category3, stock=12,
            main_image='someimage.png'
        )
           
        return super().setUp()
    
    
    def tearDown(self):
        return super().tearDown()