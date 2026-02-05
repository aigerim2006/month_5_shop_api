from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from django.db.models import Count, Avg
from django.db import transaction

from .serializers import(
    CategorySerializer,
    CategoryValidateSerializer,
    ProductSerializer,
    ProductValidateSerializer,
    ReviewSerializers,
    ReviewValidateSerializer,
    ProductListSerializer,
)

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(products_count=Count('products'))

        data = CategorySerializer(categories, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        name = serializer.validated_data.get('name')
        with transaction.atomic():
            category = Category.objects.create(name=name)
        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = (Product.objects.select_related('category').prefetch_related('reviews').annotate(rating=Avg('reviews__stars')))

        data = ProductListSerializer(products, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category')

        with transaction.atomic():
            product = Product.objects.create(
                title = title,
                description = description,
                price = price,
                category_id = category_id
            )
        return Response(
            status=status.HTTP_201_CREATED, data=ProductSerializer(product).data
        )

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializers(reviews, many=True).data
        return Response(status=status.HTTP_200_OK, data=data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product')

        with transaction.atomic():
            review = Review.objects.create(
                text=text,
                stars=stars,
                product_id=product_id
            )
        return Response(
            status=status.HTTP_201_CREATED,
            data = ReviewSerializers(review).data
        )
     
        

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(
            data={'error': 'category not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        data = CategorySerializer(category).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED, data=CategorySerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist: 
        return Response(
            data={'error': 'product not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        return Response(ProductSerializer(product).data)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category')
        product.save()
        return Response(status=status.HTTP_201_CREATED, data = ProductSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            data={'error': 'review not found!'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        return Response(ReviewSerializers(review).data)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product')
        review.save()
        return Response(status=status.HTTP_201_CREATED, data=ReviewSerializers(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

