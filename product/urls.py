from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view()),
    path('/<int:pk>', views.ProductDetailView.as_view()),
    #path('/comment', views.ProductCommentListView.as_view()),
    path('/comment', views.ProductCommentCreateView.as_view()),
    path('/<int:product_id>/comment', views.ProductSpecificCommentListView.as_view()),
    path('/like', views.LikeCreateView.as_view()),
]
