from rest_framework import serializers
from product.models import Brand, Category, Product

class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'is_active', 'description']

        

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'is_active', 'description', 'company', 'image',]

        

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['name', 'brand', 'category', 'cost_price', 'price', 'stock', 'is_active', 'image',]
