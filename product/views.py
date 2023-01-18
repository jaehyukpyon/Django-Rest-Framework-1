# from django.shortcuts import render

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
        return Response()
    
class ProductDetailView(APIView):
    
    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        print(product)
        result = {
            'name': product.name,
            'price': product.price,
            'type': product.product_type,
        }
        return Response(result)
