from product.models import Product
from ordermanagement.serializers.product import ProductSerializer
from django.conf import settings


def serialize_cart_session_data(view, request, data):
    result = {
        "id":None,
        "user":None,
        "items_count":len(data),
        "total_price":0,
        "total_discounted_price":0,
        "total_discount":0,
        "postage_fee":settings.POSTAGE_FEE if len(data) else 0,
        "final_price":0,
        "items":list()
    }
    
    product_qs = Product.objects.filter(id__in=data.keys())
    
    # Add items
    for product in product_qs:
        product_id = str(product.id)
        item = {
            "id":None,
            "cart":None,
            "item_price":product.price*data[product_id],
            "item_discounted_price":product.get_discounted_price()*data[product_id],
            "item_discount_amount":product.get_discount_amount()*data[product_id],
            "product":ProductSerializer(
                product, context=view.get_serializer_context()
            ).data,
            "quantity":data[product_id]
        }
        result["items"].append(item)
        result["total_price"] += item["item_price"]
        result["total_discounted_price"] += item["item_discounted_price"]
        result["total_discount"] += item["item_discount_amount"]
        
    result["final_price"] = result["total_discounted_price"]+result["postage_fee"]
          
    return result