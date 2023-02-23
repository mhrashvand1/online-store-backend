from django.dispatch import receiver
from account import signals as account_signals
from ordermanagement import signals as ordermanagement_signals
from account.views import AuthConfirmView
from ordermanagement.models import CartItem
from ordermanagement.views import OrderViewSet
from common.utils import send_sms


@receiver(
    signal=account_signals.user_auth_confirm_signal, 
    sender=AuthConfirmView
)
def create_cart_items(sender, request, user, *args, **kwargs):
    cart = user.cart
    session_cart = request.session.get("cart", {})
    
    # Delete old items
    cart.items.all().delete()
    
    # Create new items
    for product_id, quantity in session_cart.items():
        CartItem.objects.create(
            cart=cart, product_id=product_id, quantity=quantity
        ) 
        request.session['cart'] = {}


@receiver(
    signal=ordermanagement_signals.change_order_status_signal,
    sender=OrderViewSet
)
def send_sms_after_change_order(
    sender, 
    request, 
    order,
    new_status,
    *args, 
    **kwargs
):
    if new_status == 'paid':
        return
    
    user = order.user
    order_id = order.id
    user_full_name = user.get_full_name()
    phone_number = user.phone_number.national_number
    sms_text = "Hey {}, The status of your order ID {} changed to {}."
    sms_text = sms_text.format(user_full_name, order_id, new_status)
    
    send_sms(text=sms_text, phone_number=phone_number)