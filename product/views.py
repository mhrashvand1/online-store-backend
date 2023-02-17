from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin, 
    UpdateModelMixin
)
from product.serializers import (
    CategorySerializer,
    ImageSerializer,
    ProductReadSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductAddImageSerializer,
    ProductDeleteImageSerializer,
    ProductChargeStockSerializers
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from common.permissions import IsSuperUser 
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from product.models import Product, Category, Image
from django.db.models import Count
from product.filters import CategoryFilter
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
        return [IsAdminUser,]