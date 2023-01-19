from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('/<int:pk>', views.ProductDetailView.as_view()),
    path('/comment', views.ProductCommentListView.as_view()),
    path('/<int:product_pk>/comment', views.ProductSpecificCommentListView.as_view())
]
