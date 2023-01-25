from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductComment, Like
from .serializers import (
    ProductSerializer, 
    ProductCommentSerializer,
    ProductCommentCreateSerializer,
    LikeCreateSerializer,
)
from .paginations import ProductLargePagination

# Create your views here.

class ProductListView(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        generics.GenericAPIView,
    ):
    
    serializer_class = ProductSerializer    
    pagination_class = ProductLargePagination    
    # permission_classes = [ # 이 부분이 추가되니 get요청 보냈을 때, 아래의 get메서드 자체가 호출되지 않는다.
    #     IsAuthenticated,
    # ]
    
    def get_queryset(self):
        # if self.request.user.is_authenticated:
        
        # name = self.request.query_params.get('name')
        # products = Product.objects.all()
        # if name:
        #   products = products.filter(name__contains=name)
        
        products = Product.objects.all().prefetch_related('productcomment_set')
        # 여러 개의 결과값을 가져오는 QuerySet!!! 이 순간 DB에서 가져오지 않음
        
        if 'price' in self.request.query_params:
            price = self.request.query_params['price']
            products = products.filter(price__lte=price) # 이 순간 DB에서 가져오지 않음
            
        if 'name' in self.request.query_params:
            name = self.request.query_params['name']
            products = products.filter(name__contains=name) # 이 순간 DB에서 가져오지 않음        
            
        products = products.order_by('id') # 이 순간 DB에서 가져오지 않음
        
        return products    
    
    def get(self, request, *args, **kwargs):
        print('@@@ ProductListView - get called.')
        # Queryset
        # Serialize
        # return Response
        print(request.user)
        if self.request.user.is_authenticated:
            print('### user is successfully authenticated!')
        return self.list(request, args, kwargs)
        # else:
        #     print('### user is NOT authenticated!')
        #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    
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
    
    
class ProductCommentListView(
        mixins.ListModelMixin,
        generics.GenericAPIView,
    ):
    
    serializer_class = ProductCommentSerializer
    
    def get_queryset(self):
        products_comments = ProductComment.objects.all()
        
        # product_id = self.kwargs.get('product_id')
        # if product_id:
        #     return ProductComment.objects.filter(product_id=product_id) \
        #         .select_related('member', 'product') \
        #         .order_by('-id')
        
        #return ProductComment.objects.none()
        return products_comments
    
    def get(self, request, *args, **kwargs):
        print('@@@ TEST @@@')
        print(request.user)
        if self.request.user.is_authenticated:
            print('user is successfully authenticated!')
            
        return self.list(request, args, kwargs)

class ProductSpecificCommentListView(
        mixins.ListModelMixin,
        generics.GenericAPIView,
    ):
    
    serializer_class = ProductCommentSerializer
    
    def get_queryset(self):
        #product_id = self.kwargs.get('product_id')        
        # if product_id:
        #     # product__pk
        #     # product
        #     return ProductComment.objects.filter(product_id=self.kwargs['product_id']).order_by('-id')
        
        product_id = self.kwargs.get('product_id')
        if product_id:
            return ProductComment.objects.filter(product_id=product_id) \
                .select_related('member', 'product') \
                .order_by('-id')
        
        return ProductComment.objects.none()
        
        # return products_comments
    
    def get(self, request, *args, **kwargs):
        print(request.user)
        if self.request.user.is_authenticated:
            print('user is successfully authenticated!')
            
        return self.list(request, args, kwargs)
    
    
class ProductCommentCreateView(
        mixins.CreateModelMixin,
        generics.GenericAPIView,
    ):
    
    serializer_class = ProductCommentCreateSerializer
    
    def get_queryset(self):
        return ProductComment.objects.all()
    
    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
    
class LikeCreateView(
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    serializer_class = LikeCreateSerializer
    
    def get_queryset(self):
        return Like.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        if Like.objects.filter(member=request.user, product_id=request.data.get('product')).exists():
            Like.objects.filter(member=request.user, product_id=request.data.get('product')).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return self.create(request, args, kwargs)
    