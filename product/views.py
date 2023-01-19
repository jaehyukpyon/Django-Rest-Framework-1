from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
from .paginations import ProductLargePagination

# Create your views here.

class ProductListView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView,
    ):
    
    serializer_class = ProductSerializer
    
    pagination_class = ProductLargePagination
    
    def get_queryset(self):
        # name = self.request.query_params.get('name')
        # products = Product.objects.all()
        # if name:
        #   products = products.filter(name__contains=name)
        
        products = Product.objects.all() # 여러 개의 결과값을 가져오는 QuerySet!!! 이 순간 DB에서 가져오지 않음
        
        if 'price' in self.request.query_params:
            price = self.request.query_params['price']
            products = products.filter(price__lte=price) # 이 순간 DB에서 가져오지 않음
            
        if 'name' in self.request.query_params:
            name = self.request.query_params['name']
            products = products.filter(name__contains=name) # 이 순간 DB에서 가져오지 않음        
            
        products = products.order_by('id') # 이 순간 DB에서 가져오지 않음
        
        return products    
    
    def get(self, request, *args, **kwargs):
        # Queryset
        # Serialize
        # return Response
        return self.list(request, args, kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
    
class ProductDetailView(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, args, kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, args, kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, args, kwargs)
