from rest_framework import serializers
from product.models import Brand, Category, Product

class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'is_active', 'description']

        

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'is_active', 'description', 'image',]

        

class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = '__all__'
        fields = ['id','name', 'brand', 'category', 'cost_price', 'price', 'stock', 'is_active', 'image',]

    def update(self, instance, validated_data):
        # Atualiza o status ou outros campos específicos
        instance.stock = validated_data.get('stock', instance.stock)
        instance.save()

        return instance