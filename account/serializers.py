from rest_framework import serializers
from account.models import Location, Address
from phonenumber_field.serializerfields import PhoneNumberField
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
from rest_framework.validators import UniqueValidator
from config.settings import CODE_LENGTH
from common.utils import hash_string
from account.utils import retrieve_code
from django.contrib.auth import get_user_model

User = get_user_model()

class AddressSerializer(serializers.Serializer):
    state = serializers.CharField(allow_blank=False, allow_null=False, max_length=150, required=True)
    city = serializers.CharField(allow_blank=False, allow_null=False, max_length=150, required=True)
    full_address = serializers.CharField(allow_blank=False, allow_null=False, max_length=1200, required=True)

        
class LocationSerializer(serializers.Serializer):
    latitude = serializers.DecimalField(
        max_digits=9, decimal_places=6,
        allow_null=False, required=True, coerce_to_string=False
    )
    longitude = serializers.DecimalField(
        max_digits=9, decimal_places=6,
        allow_null=False, required=True, coerce_to_string=False
    )


class UserReadOnlySerializer(serializers.ModelSerializer):
    
    address = AddressSerializer(read_only=True, many=False)
    location = LocationSerializer(read_only=True, many=False)
  
    class Meta:
        model = User
        fields = (
            "phone_number", "first_name", "last_name", 
            "is_staff", "is_superuser", "address", "location"
        )    
    

# TODO: captcha field
class SignUpSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    address = AddressSerializer(many=False, allow_null=False, required=True)

    class Meta:
        model = User
        fields = (
            "phone_number", "first_name", "last_name",
            "address",
        )
    
    def create(self, validated_data):
        address = validated_data.pop("address")  
        try:
            with transaction.atomic():
                user = User.objects.create(**validated_data)
                user.set_password(get_random_string(length=12))
                user.save()
                Address.objects.create(
                    user=user,
                    state=address['state'],
                    city=address["city"],
                    full_address=address["full_address"]
                )
                Location.objects.create(user=user)  ## get location data later
                return user
        except:
            raise APIException("Error while creating user.")


# TODO: captcha field
class SignInSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
    )
    
    def validate_phone_number(self, value):
        
        try:
            user = User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise ValidationError(f"User with phone number {value} does not exists.")
    
        return str(user.phone_number.national_number)
 

class AuthConfirmSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
    )
    code = serializers.CharField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
        min_length=CODE_LENGTH,
        max_length=CODE_LENGTH,
    )
   
    def validate(self, data):
        phone_number = data['phone_number']

        try:
            user = User.objects.select_related("address").select_related("location"). \
                get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError(f"User with phone number {phone_number} does not exists.")
     
        phone_number = str(user.phone_number.national_number)
        stored_code = retrieve_code(phone_number=phone_number)
        raw_code = data["code"]
        hashed_code = hash_string(raw_code)
      
        if not stored_code or (hashed_code != stored_code):
            raise ValidationError("Invalid code.")
        
        data["user"] = user
        return data



class UserInfoUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, allow_null=False, required=True)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "address"]

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address")
        address = instance.address
        address.state = address_data.get("state", address.state)
        address.city = address_data.get("city", address.city)
        address.full_address = address_data.get("full_address", address.full_address)
        address.save()
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class MakeStaffSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
    )

    def validate(self, data):
        phone_number = data['phone_number']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError(f"User with phone number {phone_number} does not exists.")
        
        if user.is_staff:
            raise ValidationError(f"User with phone number {phone_number} is already staff.")   
    
        data['user'] = user
        return data
        
        
class UnMakeStaffSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(
        allow_null=False, 
        allow_blank=False, 
        required=True,
    )

    def validate(self, data):
        phone_number = data['phone_number']
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError(f"User with phone number {phone_number} does not exists.")
        
        if not user.is_staff:
            raise ValidationError(f"User with phone number {phone_number} is not staff.")   
        
        if user.is_superuser:
            raise PermissionDenied(f"User with phone number {phone_number} is a superuser.")
        
        data['user'] = user
        return data

