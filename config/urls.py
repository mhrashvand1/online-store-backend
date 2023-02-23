from django.contrib import admin
from django.urls import path, re_path, include
from common.swaggers import schema_view
from account.forms import AuthenticationForm
from django.conf import settings
from django.conf.urls.static import static


admin.site.login_form = AuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls", namespace='account')),
    path('product/', include('product.urls', namespace='product')),
    path('wallet/', include('wallet.urls', namespace='wallet')),
    path('ordermanagement/', include('ordermanagement.urls', namespace='ordermanagement')),
   # swagger urls
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += media_urls