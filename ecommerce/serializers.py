from rest_framework import serializers
from.models import Category, Product, Order

class CategorySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Product
        fields = [
            'id','name','price',
            'description','stock','category'
        ]  


class OrderSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Order
        fields = [
            'id','name','price',
            'description','stock','category'
        ]                      