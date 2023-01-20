from django.contrib import admin
from .models import Product, ProductComment, Like

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name', 'tstamp')
    # list_filter = ['product_type']
    pass    

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass