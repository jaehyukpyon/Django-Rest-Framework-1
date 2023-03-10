from django.db import models
from member.models import Member

# Create your models here.

#모델명_set
class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name="상품명")
    price = models.IntegerField(verbose_name='가격')
    product_type = models.CharField(max_length=16, verbose_name="상품유형",
                        choices=(
                            ('단품', '단품'),
                            ('세트', '세트'),
                        )
                    )
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='등록일시')
    
    def __str__(self):
        return f'Product -> name: {self.name}, price: {self.price}, product_type: {self.product_type}, tstamp: {self.tstamp}'

    class Meta:
        db_table = 'shinhan_product'
        verbose_name = '상품'
        verbose_name_plural = '상품(들)'
        
class ProductComment(models.Model):
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name='회원(맴버) PK')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품 PK')
    content = models.TextField(verbose_name="댓글 내용")
    tstamp = models.DateTimeField(auto_now_add=True, verbose_name='댓글등록일시')
    
    class Meta:
        db_table = 'shinhan_product_comment'
        verbose_name = '상품의 댓글'
        verbose_name = '상품의 댓글(들)'
        
class Like(models.Model):
    member = models.ForeignKey('member.Member', on_delete=models.CASCADE, verbose_name='회원(맴버) PK')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품 PK')
    
    class Meta:
        db_table = 'shinhan_product_like'
        verbose_name = '상품 좋아요'
        verbose_name_plural = '상품 좋아요(들)'
        