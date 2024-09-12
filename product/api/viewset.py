from django.shortcuts import get_object_or_404, render
from dj_rql.drf import RQLFilterBackend
from product.models import  Brand, Category, Product
from .filters import BrandFilterClass, CategoryFilterClass, ProductFilterClass
from rest_framework import viewsets
from .serializers import BrandModelSerializer, CategoryModelSerializer, ProductModelSerializer


# Create your views here.

class BrandModelViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = BrandFilterClass


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = CategoryFilterClass


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [RQLFilterBackend]
    rql_filter_class = ProductFilterClass