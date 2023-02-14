from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from account.serializers import (
    UserReadOnlySerializer,
    SignUpSerializer,
    SignInSerializer,
    AuthConfirmSerializer,
    UserInfoUpdateSerializer,
    MakeStaffSerializer,
    UnMakeStaffSerializer
)
from django.urls import reverse
from common.utils import get_abs_url, send_sms
from account.utils import generate_random_code, store_code, get_tokens_for_user
from rest_framework.permissions import AllowAny, IsAdminUser
from common.permissions import IsSuperUser 
from account.throttles import AuthConfirmThrottle


class SignUpView(GenericAPIView):
    
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]
    # throttle_classes
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate, SMS and Store the code
        raw_code = generate_random_code()
        phone_number = str(user.phone_number.national_number) # without +98 or 0
        send_sms(text=f"Your code is {raw_code}", phone_number=phone_number)
        store_code(phone_number=phone_number, raw_code=raw_code)
    
        return Response(
            {
                "detail":"The confirmation code was sent to the phone number 09035004342. Go to the address below",
                "url":get_abs_url(reverse("account:auth_confirm"))
            }, 
            200
        )


class SignInView(GenericAPIView):
    
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]
    # throttle_classes

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Generate, SMS and Store the code
        raw_code = generate_random_code()
        phone_number = serializer.validated_data['phone_number'] # without +98 or 0
        send_sms(text=f"Your code is {raw_code}", phone_number=phone_number)
        store_code(phone_number=phone_number, raw_code=raw_code)
    
        return Response(
            {
                "detail":"The confirmation code was sent to the phone number 09035004342. Go to the address below",
                "url":get_abs_url(reverse("account:auth_confirm"))
            }, 
            200
        )


class AuthConfirmView(GenericAPIView):
   
    serializer_class = AuthConfirmSerializer
    permission_classes = [AllowAny,]
    throttle_classes = [AuthConfirmThrottle,]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        user_data = UserReadOnlySerializer(user).data
        tokens = get_tokens_for_user(user)
        response_ = {**tokens, **user_data}
        return Response(
            response_,
            200
        )  


class StaffViewSet(GenericViewSet):
    # Only superuser has permission.
    # list, detail, makestaff, unmakestaff.
    pass

class ProfileViewSet(GenericViewSet):
    # Each user can read, update, partial update itself.
    pass 