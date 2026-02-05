from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Category
        fields = 'id name products_count'.split()

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=255)
    description = serializers.CharField()
    price = serializers.FloatField(min_value=0)
    category = serializers.IntegerField()

    def validate_category(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist! ')
        return category_id

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product = serializers.IntegerField()

    def validate_product(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist! ')
        return product_id

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = 'id title price rating category reviews'.split()
    def get_reviews(self, product):
        return ReviewSerializers(product.reviews.all(), many=True).data
    



