from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(allow_blank=False, allow_null=False, required=True)