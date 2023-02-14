from common.throttles import CustomBaseThrottle
from config.settings import CODE_EXPIRE_TIME
from common.serializers import PhoneNumberSerializer
from account.utils import retrieve_code


class AuthConfirmThrottle(CustomBaseThrottle):
    
    def __init__(self):
        self.num_requests = 5
        self.duration = CODE_EXPIRE_TIME*60  # seconds
    
    def get_cache_key(self, request, view):
        phone_number = request.data.get("phone_number")
        serializer = PhoneNumberSerializer(data={"phone_number":phone_number})
        if not serializer.is_valid():
            return
        
        phone_number = str(serializer.validated_data.get("phone_number").national_number)
        code = retrieve_code(phone_number=phone_number)
        if not code:
            return
        
        return 'throttle_%(scope)s_%(ident)s' % {
            'scope': 'auth_confirm',
            'ident': phone_number+code
        }
