from rest_framework import serializers
from wallet.models import Wallet, Payment
from common.utils import get_abs_url
from django.urls import reverse


class WalletSerializer(serializers.ModelSerializer):
    
    detail = serializers.HyperlinkedIdentityField(
        view_name="wallet:wallets-detail", lookup_field='pk',
        read_only=True,
    )
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'detail', 'created_at', 'updated_at']
        
    def get_user(self, obj):
        phone_number = str(obj.user.phone_number.national_number)
        data = {
            "phone_number":phone_number,
            "full_name":obj.user.get_full_name(),
            "url": get_abs_url(reverse("account:users-detail", kwargs={"phone_number":phone_number}))
        }
        return data
    

# Always read only
class PaymentSeralizer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(
        view_name="wallet:payments-detail", source='pk',
        read_only=True,
    )
    user = serializers.SerializerMethodField()
 
    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'amount', 'status', 
            'error_code', 'error_message', 'detail', 'created_at', 'updated_at'
        ]
        
    def get_user(self, obj):
        phone_number = str(obj.user.phone_number.national_number)
        data = {
            "phone_number":phone_number,
            "full_name":obj.user.get_full_name(),
            "url": get_abs_url(reverse("account:users-detail", kwargs={"phone_number":phone_number}))
        }
        return data
    
    
class FakeChargeWalletSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1000, required=True, allow_null=False)
    