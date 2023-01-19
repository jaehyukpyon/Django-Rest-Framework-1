from rest_framework import serializers

from .models import Product, ProductComment

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__' # ['id', 'name']

# class ProductSerialiser(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     price = serializers.IntegerField()

class ProductCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductComment
        fields = '__all__'