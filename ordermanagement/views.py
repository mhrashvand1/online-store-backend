from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from ordermanagement.serializers import CartSerializer
from rest_framework.mixins import RetrieveModelMixin


class CartViewSet(GenericViewSet):
    
    permission_classes = [AllowAny,]
    serializer_class = CartSerializer
    
    
    @action(detail=False, methods=['get',], url_name='mycart', url_path='mycart')
    def mycart(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.authenticated_mycart(request, *args, **kwargs)
        else:
            return self.anonymous_mycart(request, *args, **kwargs)
            
    def authenticated_mycart(self, request, *args, **kwargs):
        cart = request.user.cart
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def anonymous_mycart(self, request, *args, **kwargs):
        pass
    
    
    
    @action(detail=False, methods=['post',], url_name='add_product', url_path='add_product')
    def add_product(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.authenticated_add_product(request, *args, **kwargs)
        else:
            return self.anonymous_add_product(request, *args, **kwargs)
    
    def authenticated_add_product(self, request, *args, **kwargs):
        pass
    
    def anonymous_add_product(self, request, *args, **kwargs):
        pass
        
        
        
    @action(detail=False, methods=['post',], url_name='subtract_product', url_path='subtract_product')
    def subtract_product(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.authenticated_subtract_product(request, *args, **kwargs)
        else:
            return self.anonymous_subtract_product(request, *args, **kwargs)
        
    def authenticated_subtract_product(self, request, *args, **kwargs):
        pass
    
    def anonymous_subtract_product(self, request, *args, **kwargs):
        pass