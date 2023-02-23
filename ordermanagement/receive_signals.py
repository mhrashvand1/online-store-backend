from django.dispatch import receiver
from account import signals
from account.views import AuthConfirmView
from ordermanagement.models import CartItem


@receiver(signal=signals.user_auth_confirm_signal, sender=AuthConfirmView)
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
        del request.session['cart']
