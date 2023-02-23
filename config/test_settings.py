from config.settings import * 

print("\nconfig.test_settings.py is settings module\n")

# One-time code config
CODE_EXPIRE_TIME = 3 # minutes 
CODE_LENGTH = 6 # max:20

# Simple JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10), 
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "AUTH_HEADER_TYPES": ("Bearer", "jwt", "JWT",),
}

# Product
PRODUCT_MAX_IMAGES_COUNT = 10  # except main image

# Cart 
MAX_CART_ITEMS = 5
MAX_ITEM_QUANTITY = 5
ANONYMOUS_CART_EXPIRATION = 7 # days

# Postage
POSTAGE_FEE = 15000 # Toman