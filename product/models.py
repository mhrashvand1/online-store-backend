from django.db import models
from common.models import BaseModel, UUIDBaseModel
from django.utils.translation import gettext_lazy as _ 
import os
import time

def get_main_image_path(instance, filename):
    suffix = filename.split('.')[-1]
    name = 'mainimage' + str(time.time()).split('.')[0] + '.' + suffix
    return os.path.join(str(instance.id), 'images', name)

class Product(UUIDBaseModel):
    
    name = models.CharField(
        max_length=255, blank=False, null=False, verbose_name=_('name')
    )
    description = models.CharField(
        max_length=3500, blank=False, null=False, verbose_name=_('description')
    )
    price = models.PositiveBigIntegerField(blank=False, null=False, verbose_name=_('price'))
    slug = models.SlugField(
        max_length=255, null=False, blank=False,
        unique=True, db_index=True, verbose_name=_('slug')
    )
    category = models.ForeignKey(
        to='product.Category', on_delete=models.SET_NULL, null=True,
        related_name='products', verbose_name=_('category')
    )
    main_image = models.ImageField(blank=False, null=False, upload_to=get_main_image_path, verbose_name=_('main image')) 
    stock = models.PositiveIntegerField(null=False, blank=False, default=0, verbose_name=_('stock'))
    
    def __str__(self) -> str:
        return f"{str(self.id)}-{self.name}"
    
    class Meta:
        db_table = 'Product'
        verbose_name = _("product")
        verbose_name_plural = _("products")
        
        
class Category(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True, verbose_name=_('name'))
    slug = models.SlugField(max_length=255, blank=False, null=False, unique=True, db_index=True, verbose_name=_('slug'))
    description = models.CharField(max_length=3500, blank=False, null=False, verbose_name=_('description'))
    
    def __str__(self) -> str:
        return f"{str(self.id)}-{self.name}"
    
    class Meta:
        db_table = 'Category'
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        
  
def get_image_path(instance, filename):
    suffix = filename.split('.')[-1]
    name = str(time.time()).split('.')[0] + '.' + suffix
    return os.path.join(str(instance.product.id), 'images', 'otherimages', name)
      
class Image(BaseModel):
    product = models.ForeignKey(
        to='product', on_delete=models.CASCADE, related_name='images', verbose_name=_('product')  
    )
    image = models.ImageField(null=False, blank=False, upload_to=get_image_path, verbose_name=_('image'))
    
    def __str__(self) -> str:
        return str(self.image.url)
    
    class Meta:
        db_table = 'Image'
        verbose_name = _("image")
        verbose_name_plural = _("image")