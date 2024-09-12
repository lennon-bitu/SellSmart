from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views
from product.api.viewset import BrandModelViewSet, CategoryModelViewSet, ProductModelViewSet

app_name ='product'

router = DefaultRouter()
router.register('brands', BrandModelViewSet)
router.register('categories', CategoryModelViewSet)
router.register('products', ProductModelViewSet)

product_urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('valid/', views.product_valid_create, name='valid'),
]
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('products/', include(product_urlpatterns)),


]