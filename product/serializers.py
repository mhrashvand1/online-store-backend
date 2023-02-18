from rest_framework import serializers
from product.models import Product, Category, Image
from common.utils import get_abs_url
from django.db import transaction
from rest_framework.exceptions import APIException, ValidationError
from django.db.models import Count
from config.settings import PRODUCT_MAX_IMAGES_COUNT
from django.urls import reverse
from urllib.parse import urlencode


class CategorySerializer(serializers.ModelSerializer):
    
    products = serializers.SerializerMethodField()
    detail = serializers.HyperlinkedIdentityField(
        view_name='product:categories-detail', 
        lookup_field="slug",  read_only=True,
    )
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'products', 'detail']
    
    def get_products(self, obj):
        id = str(obj.id)
        url = reverse('product:products-list')
        return get_abs_url(url) + '?' + urlencode({"category":id})
    

class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = ['id', 'product', 'image']


class ProductReadSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(many=False, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    detail = serializers.HyperlinkedIdentityField(
        view_name='product:products-detail', 
        lookup_field="slug", read_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'slug', 
            'price', 'stock', 'main_image', 'category',
            'images', "created_at", "updated_at", "detail"
        ]
    
    
class ProductCreateSerializer(serializers.ModelSerializer):
    
    images = serializers.ListField(
        required=False,
        allow_empty=False,
        allow_null=False,
        child=serializers.ImageField(required=True, allow_null=False),
        max_length=PRODUCT_MAX_IMAGES_COUNT,
        write_only=True
    )
    category = serializers.PrimaryKeyRelatedField(
        allow_null=False, 
        queryset=Category.objects.all(), 
        required=True
    )
    detail = serializers.HyperlinkedIdentityField(
        view_name='product:products-detail', 
        lookup_field="slug", read_only=True,
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'slug', 
            'price', 'stock', 'main_image', 'category',
            'images', "created_at", "updated_at", "detail"
        ]
    
    def create(self, validated_data):
        images = validated_data.get('images', None)
        if images:
            del validated_data['images']
        else:
            images = []
                
        try:
            with transaction.atomic():
                product = Product.objects.create(**validated_data)
                for i in images:
                    Image.objects.create(product=product, image=i)
        except:
            raise APIException("Error while creating product.")
        
        return product
   
    
class ProductUpdateSerializer(serializers.ModelSerializer):

    category = serializers.PrimaryKeyRelatedField(
        allow_null=False, 
        queryset=Category.objects.all(), 
        required=True
    )
    detail = serializers.HyperlinkedIdentityField(
        view_name='product:products-detail', 
        lookup_field="slug", read_only=True,
    )
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'slug', 
            'price', 'stock', 'main_image', 'category',
            "created_at", "updated_at", "detail"
        ]
    

class ProductAddImageSerializer(serializers.Serializer):
    
    image = serializers.ImageField(required=True, allow_null=False)
    
    def validate(self, data):
        product = self.context['product']
        img_count = product.images.aggregate(Count('id'))['id__count']
        if not img_count < PRODUCT_MAX_IMAGES_COUNT:
            raise ValidationError(f"Reaching the image limit {PRODUCT_MAX_IMAGES_COUNT}.")
        return data
    
    def create(self, validated_data):
        product = self.context['product']
        image = validated_data['image']
        Image.objects.create(product=product, image=image)
        return product
        

class ImageRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        slug = self.context['view'].kwargs['slug']
        queryset = Image.objects.filter(product__slug=slug)
        return queryset

class ProductDeleteImageSerializer(serializers.Serializer):
    
    image = ImageRelatedField(required=True, allow_null=False)
        
    def delete(self):
        image = self.validated_data['image']
        image.delete()


class ProductChargeStockSerializers(serializers.Serializer):
    count = serializers.IntegerField(min_value=1, required=True, allow_null=False)
    
    def perform_charge(self):
        product = self.context['product']
        product.stock += self.validated_data['count']
        product.save()