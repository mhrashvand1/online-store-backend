from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from ordermanagement.serializers.cart import (
    CartSerializer,
    CartAddProductSerializer,
    CartSubtractProductSerialzier,
)
from ordermanagement.serializers.order import (
    OrderSerializer,
    OrderChangeStatusSerializer, 
)
from ordermanagement.serializers.checkout import CheckoutSerializer
from ordermanagement.utils import serialize_cart_session_data
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ordermanagement.permissions import OrderDeletePermission
from ordermanagement.filters import OrderFilter
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from ordermanagement.models import Order
from django.db import transaction
from rest_framework.exceptions import APIException
from ordermanagement.signals import change_order_status_signal
from django.db.models import F, Q, Sum, Count


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
        response_msg = {
            "type":"authenticated-user",
            **serializer.data
        }
        return Response(response_msg)
    
    def anonymous_mycart(self, request, *args, **kwargs):
        data = request.session.get('cart', {})
        data = serialize_cart_session_data(self, request, data)     
        response_msg = {
            "type":"anonymous-user",
            **data
        }
        return Response(response_msg)
    
    
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
            "type":"authenticated-user",
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
            "type":"anonymous-user",
            **serialize_cart_session_data(
                self,
                request,
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
            "type":"authenticated-user",
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
            "type":"anonymous-user",
            **serialize_cart_session_data(
                self,
                request,
                request.session.get('cart', {})
            )
        }
        return Response(response_msg) 
    

################################################################
################################################################
####################### CheckoutView ###########################
################################################################

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated,]    
    
    def get(self, request, *args, **kwargs):
        cart = request.user.cart
        user_wallet = request.user.wallet
        serializer = CheckoutSerializer(
            data={},
            context={
                **self.get_serializer_context(),
                "cart":cart, 
                'user_wallet':user_wallet
            }
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.perform_checkout()
        response_msg = {
            "detail":"The purchase has been successfully completed and your order has been registered",
            "order":OrderSerializer(order, context=self.get_serializer_context()).data
        }
        return Response(response_msg)

    def get_serializer_context(self):
        return {
            "request":self.request, 
            "view":self,
            "format":self.format_kwarg, 
        }

################################################################
################################################################
####################### OrderViewSet ###########################
################################################################

class OrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    search_fields = [
        'user__first_name', 
        'user__last_name',
        'user__phone_number',
        'items__p_name',
    ] 
    ordering_fields = [
        'user', 
        'status',
        'postage_fee', 
        'items_count', 
        'total_price', 
        'total_discounted_price',
        'total_discount',
        'final_price',
    ] 
    
    def get_serializer_class(self):
        if self.action == 'change_status':
            return OrderChangeStatusSerializer
        return OrderSerializer
    
    @property
    def permission_classes(self):
        if self.action == 'destroy':
            return [IsAuthenticated, OrderDeletePermission]
        elif self.action == 'change_status':
            return [IsAuthenticated, IsAdminUser,]
        return [IsAuthenticated,]
    
    
    def get_queryset(self):
        user = self.request.user
        user_is_admin = user.is_staff
        
        queryset = Order.all_objects.prefetch_related(
            'items', 
            'items__product',
            'user',
            'user__address',
            'user__location',
        )
        
        if self.action in ['deleted_orders_list', 'deleted_orders_detail']:
            if user_is_admin:
                queryset = queryset.filter(status='deleted')
            else:
                queryset = queryset.filter(
                    status='deleted', user=user
                )
        else:
            if user_is_admin:
                queryset = queryset.exclude(status='deleted')
            else:
                queryset = queryset.filter(user=user).exclude(status='deleted')
        
        # Annotate statistic fields
        queryset = queryset.annotate(
            items_count=Count('items'),
            total_price=Sum(
                F("items__quantity")*F('items__p_price')
            ),
            total_discounted_price=Sum(
                F("items__quantity")*
                (
                    F('items__p_price') - 
                    F('items__p_price')*F('items__p_discount_percent')/100
                )
            ),
            total_discount=Sum(
                F("items__quantity")*
                (
                    F("items__p_price")*F("items__p_discount_percent")/100
                )
            ),
            final_price=F('total_discounted_price') + F('postage_fee')
        )
                 
        return queryset
    
    
    def perform_destroy(self, instance):
        order = instance
        user = order.user
        user_wallet = user.wallet
        try:
            with transaction.atomic():
                # Return the amount to the wallet
                user_wallet.balance += order.get_final_price()
                user_wallet.save()
                
                # Returns the number of stock to the products
                for item in order.items.all():
                    product = item.product
                    if product:
                        product.stock += item.quantity
                        product.save()
                        
                # Delete the order
                order.delete(soft=True)
                
        except:
            raise APIException("Error while deleting order.")
    
    
    @action(detail=True, methods=['put',], url_name='change_status', url_path='change_status')
    def change_status(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']
        order = self.get_object()
        order.status = new_status
        order.save()
        # Sending signal for change status.
        change_order_status_signal.send(
            self.__class__,
            request=request,
            order=order,
            new_status=new_status
        )
        
        response_msg = OrderSerializer(order, context=self.get_serializer_context()).data
        return Response(response_msg)
        
        
    @action(
        detail=False,
        methods=['get',],
        url_name='deleted_orders_list',
        url_path='deleted_orders_list'
    )
    def deleted_orders_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    @action(
        detail=False, 
        methods=['get',], 
        url_name='deleted_orders_detail', 
        url_path='deleted_orders_detail'
    )
    def deleted_orders_detail(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)