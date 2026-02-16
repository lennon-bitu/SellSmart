from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from order.models import Order
from .serializers import OrderSerializer

class PublicOrderListView(APIView):
    """
    View para listar todos os pedidos publicamente acessíveis.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class PublicOrderDetailView(APIView):
    """
    View para detalhar um pedido publicamente acessível.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
