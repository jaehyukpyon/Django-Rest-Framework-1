from django.contrib import admin
from .models import Product, ProductComment

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    pass