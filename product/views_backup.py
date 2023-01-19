# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product

# Create your views here.

class ProductListView(APIView):
    
    def get(self, request, *args, **kwargs):
        # 
        print(request.query_params)
        
        # QuerySet
        ret = [ ]
        
        # 모든 상품을 리스트로 만들어서 반환, id 속성으로 정렬해서
        # products = Product.objects.all().order_by('id')
        products = Product.objects.all() # 여러 개의 결과값을 가져오는 QuerySet!!! 이 순간 DB에서 가져오지 않음
        
        if 'price' in request.query_params:
            price = request.query_params['price']
            products = products.filter(price__lte=price) # 이 순간 DB에서 가져오지 않음
            
        if 'name' in request.query_params:
            name = request.query_params['name']
            products = products.filter(name__contains=name) # 이 순간 DB에서 가져오지 않음
        
            
        products = products.order_by('id') # 이 순간 DB에서 가져오지 않음
        
        for product in products:
            p = {
                'id': product.id, # id에 접근하는 순간 위의 DB 접근 코드를 전부 실행하고 가져온다.
                'name': product.name,
                'price': product.price,
                'type': product.product_type,
            }
            ret.append(p)

        return Response(ret)
    
    #def get(self, request, *args, **kwargs):
        
    
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
        
        # kwargs['pk']
        
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
        
        # dirty = False
        # for field, value in request.data.items():
        #     if field not in [f.name for f in product._meta.get_fields()]:
        #         continue

        #     dirty = dirty or (value != getattr(product, field))
        #     setattr(product, field, value)
        
        keys = list(request.data)
        print('keys -> ', keys)
        
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
