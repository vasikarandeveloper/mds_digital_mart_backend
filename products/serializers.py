from rest_framework import serializers

from .models import (
    Product,
    Wishlist,
    Review
)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product

        fields = '__all__'


class WishlistSerializer(serializers.ModelSerializer):

    product = ProductSerializer(
        read_only=True
    )

    class Meta:

        model = Wishlist

        fields = [
            'id',
            'product',
            'created_at'
        ]


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:

        model = Review

        fields = [
            'id',
            'username',
            'rating',
            'comment',
            'created_at'
        ]