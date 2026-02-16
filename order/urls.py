from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from order.api.viewset import OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

order_urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    #path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('create/', views.create_order, name='order_create'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('update-status/<int:pk>/', views.order_update_status, name='order_update_status'),
]

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', include(order_urlpatterns)),

]


