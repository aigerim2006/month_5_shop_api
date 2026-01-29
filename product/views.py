from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from django.db.models import Count 

from .serializers import(
    CategorySerializer,
    ProductSerializer,
    ReviewSerializers,
    ProductListSerializer,
)

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.annotate(products_count=Count('products'))

    data = CategorySerializer(categories, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.select_related('category').prefetch_related('reviews').all()

    data = ProductListSerializer(products, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewSerializers(reviews, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(
            data={'error': 'category not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = CategorySerializer(category, many=False).data
    return Response(data=data)



        
@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist: 
        return Response(
            data={'error': 'product not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = ProductSerializer(product, many=False).data
    return Response(data=data)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            data={'error': 'review not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    data = ReviewSerializers(review, many=False).data
    return Response(data=data)


