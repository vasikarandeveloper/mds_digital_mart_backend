from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet

router = DefaultRouter()

router.register('products', ProductViewSet,basename='products')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('router.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/cart/', include('cart.urls'))
]
