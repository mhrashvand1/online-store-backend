from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from ordermanagement.serializers import (
    CartSerializer,
    CartAddProductSerializer,
    CartSubtractProductSerialzier,
)


class CartViewSet(GenericViewSet):
    
    permission_classes = [AllowAny,]    
    
    def get_serializer_class(self):
        if self.action == 'add_product':
            return CartAddProductSerializer
        elif self.action == 'subtract_product':
            return CartSubtractProductSerialzier
        else:
            return CartSerializer
        
    #####################################################
    ##################### get cart ######################

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
        data = request.session.get('cart', {})
        data = self.serialize_cart_session_data(data)
        return Response(data)
    
    @staticmethod
    def serialize_cart_session_data(data):
        # TODO: calculate price, ...
        ...
        return data
    
    #####################################################
    #################### add product ####################
    
    @action(detail=False, methods=['post',], url_name='add_product', url_path='add_product')
    def add_product(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.authenticated_add_product(request, *args, **kwargs)
        else:
            return self.anonymous_add_product(request, *args, **kwargs)
    
    
    def authenticated_add_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_add_product()
        response_msg = {
            "detail":"Product added successfully",
            **CartSerializer(
                request.user.cart, 
                context=self.get_serializer_context()
            ).data
        }
        return Response(response_msg)
    
    
    def anonymous_add_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_add_product()
        response_msg = {
            "detail":"Product added successfully",
            **self.serialize_cart_session_data(
                request.session.get('cart', {})
            )
        }
        return Response(response_msg)        
        
    ##########################################################
    #################### subtract product ####################
           
    @action(detail=False, methods=['post',], url_name='subtract_product', url_path='subtract_product')
    def subtract_product(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.authenticated_subtract_product(request, *args, **kwargs)
        else:
            return self.anonymous_subtract_product(request, *args, **kwargs)

     
    def authenticated_subtract_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_subtract_product()
        response_msg = {
            "detail":"Product subtracted successfully",
            **CartSerializer(
                request.user.cart, 
                context=self.get_serializer_context()
            ).data
        }
        return Response(response_msg)   
   
    
    def anonymous_subtract_product(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.perform_subtract_product()
        response_msg = {
            "detail":"Product subtracted successfully",
            **self.serialize_cart_session_data(
                request.session.get('cart', {})
            )
        }
        return Response(response_msg) 