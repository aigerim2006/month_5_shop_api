from rest_framework import serializers
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only = True)
    class Meta:
        model = Category
        fields = 'id name products_count'.split()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text stars product'.split()


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = 'id title price rating category reviews'.split()
    def get_reviews(self, product):
        return ReviewSerializers(product.reviews.all(), many=True).data
    



