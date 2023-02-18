from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin, 
    UpdateModelMixin
)
from account.serializers import (
    UserReadOnlySerializer,
    SignUpSerializer,
    SignInSerializer,
    AuthConfirmSerializer,
    UserInfoUpdateSerializer,
    MakeStaffSerializer,
    UnMakeStaffSerializer,
    LocationSerializer,
)
from django.urls import reverse
from common.utils import get_abs_url, send_sms
from account.utils import generate_random_code, store_code, get_tokens_for_user
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from common.permissions import IsSuperUser 
from account.throttles import AuthConfirmThrottle
from django.contrib.auth import get_user_model
from rest_framework.decorators import action


User = get_user_model()


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


class UserViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):  
    
    @property
    def permission_classes(self):
        if self.action in ['makestaff', 'unmakestaff',]:
            return [IsSuperUser,]
        return [IsAuthenticated,]
    
    lookup_field = 'phone_number'
    filterset_fields = ['is_staff', 'is_superuser',]
    search_fields = ['phone_number', 'first_name', 'last_name',]
        
    def get_serializer_class(self):
        if self.action == 'makestaff':
            return MakeStaffSerializer
        elif self.action == 'unmakestaff':
            return UnMakeStaffSerializer
        else:
            return UserReadOnlySerializer
        
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = User.objects.prefetch_related("address") \
                .prefetch_related("location").prefetch_related("wallet").all()
        else:
            queryset = User.objects.prefetch_related("address") \
                .prefetch_related("location").prefetch_related("wallet").filter(id=user.id)  
        return queryset
    
    @action(detail=False, methods=['put',], url_name='makestaff', url_path='makestaff')
    def makestaff(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        user.is_staff = True
        user.save()
        phone_number = serializer.validated_data['phone_number'].national_number
        response_ = {"detail":f"The user with the phone number {phone_number} has successfully become an staff(admin)."}
        return Response(response_, 200)
        
    @action(detail=False, methods=['put',], url_name='unmakestaff', url_path='unmakestaff')
    def unmakestaff(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        user.is_staff = False
        user.save()
        phone_number = serializer.validated_data['phone_number'].national_number
        response_ = {"detail":f"The user with phone number {phone_number} has successfully remove from being an staff(admin)."}
        return Response(response_, 200)



class ProfileViewSet(
    RetrieveModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    
    permission_classes = [IsAuthenticated,]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserReadOnlySerializer
        return UserInfoUpdateSerializer
    
    def get_object(self):
        obj = User.objects.select_related("address").select_related("location"). \
            get(phone_number=self.request.user.phone_number)
        return obj


class GetLocationView(GenericAPIView):
    
    permission_classes = [IsAuthenticated,]
    serializer_class = LocationSerializer
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.location)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        location_obj = request.user.location
        location_obj.latitude = data.get("latitude", location_obj.latitude)
        location_obj.longitude = data.get("longitude", location_obj.longitude)
        location_obj.save()
        return Response(serializer.data)