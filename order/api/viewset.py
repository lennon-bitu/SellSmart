from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from order.models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, criar, atualizar, deletar e detalhar pedidos.
    Suporta todos os métodos: GET, POST, PUT, PATCH, DELETE.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna os pedidos do usuário autenticado.
        """
        return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        POST: Criação de novo pedido.
        O cliente será atribuído automaticamente ao usuário autenticado.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Define o cliente como o usuário autenticado
        serializer.save(customer=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        PUT: Atualização de pedido.
        Atualiza todos os campos do pedido.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE: Remover um pedido existente.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """
        GET: Detalhar um pedido específico.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        GET: Listar todos os pedidos do usuário autenticado.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
