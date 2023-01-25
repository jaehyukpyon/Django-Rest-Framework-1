from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Product, ProductComment, Like

class ProductSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField() # client에게 데이터를 줄 때만 사용된다. 
    
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
    product_name = serializers.SerializerMethodField()
    member_username = serializers.SerializerMethodField()
    
    def get_product_name(self, obj):
        return obj.product.name
    
    def get_member_username(self, obj):
        return obj.member.username
    
    def validate(self, data):
        print('### ProductCommentSerializer - validate called.')
        for key, value in data.items():
            print(f'@@@ key: {key}, value:{value}')
    
    class Meta:
        model = ProductComment
        fields = '__all__'
        
# ProductCommentSerializer():
#     id = IntegerField(label='ID', read_only=True)
#     content = CharField(label='댓글 내용', style={'base_template': 'textarea.html'})
#     tstamp = DateTimeField(label='댓글등록일시', read_only=True)
#     member = PrimaryKeyRelatedField(label='회원(맴버) PK', queryset=Member.objects.all())
#     product = PrimaryKeyRelatedField(label='상품 PK', queryset=Product.objects.all())

class ProductCommentCreateSerializer(serializers.ModelSerializer):
    
    member = serializers.HiddenField(
        default=serializers.CurrentUserDefault(), # hiddenfield는 default 속성이 꼭 필요하다. 사용자로부터 받더라도 그 값을 쓰는 게 아닌 default로 설정된 값을 사용한다.
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
