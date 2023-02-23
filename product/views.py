from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from product.serializers import (
    CategorySerializer,
    ProductReadSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductAddImageSerializer,
    ProductDeleteImageSerializer,
    ProductChargeStockSerializers
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from product.models import Product, Category
from django.db.models import Count
from product.filters import CategoryFilter, ProductFilter
from rest_framework.permissions import SAFE_METHODS


class CategoryViewSet(ModelViewSet):
    
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    search_fields = ['name', 'description',]
    ordering_fields = ['product_count',]
    
    def get_queryset(self):
        qs = Category.objects.annotate(
            product_count=Count('products')
        ).all()
        return qs
    
    @property
    def permission_classes(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny,]
        return [IsAuthenticated ,IsAdminUser,]
    
    
class ProductViewSet(ModelViewSet):
    
    lookup_field = 'slug'
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name', 'category__description']
    ordering_fields = ['price', 'stock', ]

    def get_queryset(self):
        return Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductUpdateSerializer
        elif self.action == 'addimage':
            return ProductAddImageSerializer
        elif self.action == 'deleteimage':
            return ProductDeleteImageSerializer
        elif self.action == 'chargestock':
            return ProductChargeStockSerializers
        else:
            return ProductReadSerializer
    
    @property
    def permission_classes(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny,]
        return [IsAuthenticated, IsAdminUser,]
    
    @action(detail=True, methods=['put',], url_name='addimage', url_path='addimage')
    def addimage(self, request, *args, **kwargs):
        product = self.get_object()
        serializer_class = self.get_serializer_class()
        context = {**self.get_serializer_context(), "product":product}
        serializer = serializer_class(data=request.data, context=context)        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_msg = {"detail":"The image has been successfully added to the product."}
        return Response(response_msg, 200)        
    
    @action(detail=True, methods=['put',], url_name='deleteimage', url_path='deleteimage')
    def deleteimage(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        response_msg = {"detail":"The image has been successfully removed from the product"}
        return Response(response_msg, 200)  
    
    @action(detail=True, methods=['put',], url_name='chargestock', url_path='chargestock')
    def chargestock(self, request, *args, **kwargs):
        product = self.get_object()
        serializer_class = self.get_serializer_class()
        context = {**self.get_serializer_context(), "product":product}
        serializer = serializer_class(data=request.data, context=context)        
        serializer.is_valid(raise_exception=True) 
        serializer.perform_charge()
        response_msg = {"detail":"The stock of the product has been charged successfully."}
        return Response(response_msg, 200) 