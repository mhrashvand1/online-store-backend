from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.views import APIView
from rest_framework.decorators import action
from wallet.filters import WalletFilter, PaymentFilter
from wallet.models import Wallet, Payment
from wallet.serializers import (
    WalletSerializer, 
    PaymentSeralizer,
    FakeChargeWalletSerializer
)
from common.permissions import IsSuperUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework.exceptions import APIException


class WalletViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    
    serializer_class = WalletSerializer
    filterset_class = WalletFilter
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name',]
    ordering_fields = ['balance',]
    
    @property
    def permission_classes(self):
        if self.action in ['update', 'partial_update']:
            return [IsSuperUser,]
        return [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Wallet.objects.prefetch_related("user").all()
        else:
            queryset = Wallet.objects.select_related("user").filter(user=user)
        return queryset


    @action(detail=False, methods=['get',], url_name='mywallet', url_path='mywallet')
    def mywallet(self, request, *args, **kwargs):
        instance = request.user.wallet
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    


class PaymentViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet 
):
    
    serializer_class = PaymentSeralizer
    filterset_class = PaymentFilter
    search_fields = ['error_message', 'user__phone_number', 'user__first_name', 'user__last_name',]
    ordering_fields = ['amount', 'status',]
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Payment.objects.prefetch_related("user").all()
        else:
            queryset = Payment.objects.prefetch_related("user").filter(user=user)
        return queryset     
   
    @action(detail=False, methods=['get',], url_name='mypayments', url_path='mypayments')
    def mypayments(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        
        if user.is_staff:
            queryset = queryset.filter(user=user)
        
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FakeChargeWalletView(APIView):
    
    serializer_class = FakeChargeWalletSerializer
    permission_classes = [IsAuthenticated,]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        user = request.user
        wallet = user.wallet
        try:
            with transaction.atomic():
                wallet.balance += amount
                wallet.save()
                Payment.objects.create(user=user, amount=amount) 
            message = {"detail":f"Your wallet was charged {amount} Tomans"}
            response_ = {**message, **WalletSerializer(wallet).data}
            return Response(response_, 200)
        except:
            raise APIException("Error while charging the wallet.")


####################################################
######### TODO: Implement Payment gateway. #########
####################################################

class ChargeWalletView(APIView):
    pass  

class ChatgeWalletViewConfirm(APIView):
    pass 