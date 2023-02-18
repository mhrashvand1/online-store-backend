from rest_framework import serializers
from wallet.models import Wallet, Payment
from common.utils import get_abs_url
from django.urls import reverse


class WalletSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance']
        
    def get_user(self, obj):
        phone_number = str(obj.user.phone_number.natiobal_number)
        data = {
            "phone_number":phone_number,
            "full_name":obj.user.get_full_name(),
            "url": get_abs_url(reverse("account:users-detail", kwargs={"phone_number":phone_number}))
        }
        return data
    

# Always read only
class PaymentSeralizer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
 
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'status', 'error_code', 'error_message']
        
    def get_user(self, obj):
        phone_number = str(obj.user.phone_number.natiobal_number)
        data = {
            "phone_number":phone_number,
            "full_name":obj.user.get_full_name(),
            "url": get_abs_url(reverse("account:users-detail", kwargs={"phone_number":phone_number}))
        }
        return data