# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product

# Create your views here.

class ProductListView(APIView):
    
    def get(self, request, *args, **kwargs):
        ret = [ ]
        
        # 모든 상품을 리스트로 만들어서 반환, id 속성으로 정렬해서
        products = Product.objects.all().order_by('id')
        
        for product in products:
            p = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'type': product.product_type,
            }
            ret.append(p)

        return Response(ret)
    
    def post(self, request, *args, **kwargs):
        print('request.data -> ',request.data)
        print('type(request.data) -> ', type(request.data))
        print("type(request.data.get('name') -> ", type(request.data.get('name')))
        
        name = request.data.get('name')
        price = request.data.get('price')
        product_type = request.data.get('product_type')
        
        new_product = Product(
            name = name,
            price = price,
            product_type = product_type
        )
        
        new_product.save()
        return Response({
            'id': new_product.id,
            'name': new_product.name,
            'price': new_product.price,
            'type': new_product.product_type,
        }, status=status.HTTP_201_CREATED)
        
    
class ProductDetailView(APIView):
    
    def get(self, request, pk, *args, **kwargs):
        
        try:            
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        print(product)
        result = {
            'name': product.name,
            'price': product.price,
            'type': product.product_type,
        }
        return Response(result)
    
    def delete(self, request, pk, *args, **kwargs):
        if Product.objects.filter(pk=pk).exists():
            product = Product.objects.get(pk=pk)
            product.delete()
        return Response({
            'id': pk
        }, status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request, pk, *args, **kwargs):
        if not Product.objects.filter(pk=pk).exists():
            return Response({
                'id': pk
            }, status=status.HTTP_404_NOT_FOUND)
            
        product = Product.objects.get(pk=pk)
        keys = list(request.data)
        print('keys -> ',keys)
        
        for key in keys:
            value = request.data.get(key)
            setattr(product, key, value)
            
        product.save()
        
        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'product_type': product.product_type
        }, status=status.HTTP_200_OK)
