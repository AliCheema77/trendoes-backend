from rest_framework.throttling import UserRateThrottle

class ProductListSellThrottle(UserRateThrottle):
    scope = 'custom_ip'

class ProductDetailThrottle(UserRateThrottle):
    scope = 'product_detail'