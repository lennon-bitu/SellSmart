from django.shortcuts import get_object_or_404, render
from rest_framework.permissions import IsAuthenticated
from product.models import  Brand, Category, Product
from rest_framework import viewsets
from .serializers import BrandModelSerializer, CategoryModelSerializer, ProductModelSerializer

# from dj_rql.drf import RQLFilterBackend
# from .filters import BrandFilterClass, CategoryFilterClass, ProductFilterClass


# Create your views here.

class BrandModelViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [RQLFilterBackend]
    # rql_filter_class = BrandFilterClass


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [RQLFilterBackend]
    # rql_filter_class = CategoryFilterClass


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [RQLFilterBackend]
    # rql_filter_class = ProductFilterClass
