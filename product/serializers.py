from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, ProductComment, Like

class ProductSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    
    # get_XXXX get_필드명 이런 식으로,
    #self ->
    def get_comment_count(self, obj):   
        print('type(obj) >> ', type(obj))  
        return obj.productcomment_set.all().count()                                   
        # return ProductComment.objects.filter(product=obj).count() # product_id=obj.id
    
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

class ProductCommentCreateSerializer(serializers.ModelSerializer):
    
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        required=False
    )
    
    # validate_xxx >> member 필드를 검증할 때 사용하는 함수이구나
    def validate_member(self, value):
        print('value >> ', value)
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required.')
        return value
    
    # def validate(self, attrs):
    #     print('attrs >> ', attrs)
    #     request = self.context['request']
    #     print('request.user >> ', request.user)
        
    #     if request and request.user.is_authenticated:
    #         attrs['member'] = request.user  
    #     else:
    #         raise ValidationError('member is required.')                
    #     return attrs
    class Meta:
        model = ProductComment
        fields = '__all__'    
        extra_kwargs = {
            'member': {
                'required': False,
            },
        }    
        
        
class LikeCreateSerializer(serializers.ModelSerializer):
    # member = serializer.IntegerField()
    
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        required=False
    )  
    
    def validate_member(self, value):
        print('value >> ', value) # request.user
        if not value.is_authenticated:
            raise serializers.ValidationError('member is required.')
        return value
    
    class Meta:
        model = Like
        fields = '__all__'
