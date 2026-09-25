from datetime import timedelta

from django.utils import timezone

from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework.views import APIView

from products.models import Product

from .models import (
    Cart,
    CartItem
)

from .serializers import CartSerializer


class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get(
            'product_id'
        )

        quantity = int(
            request.data.get(
                'quantity',
                1
            )
        )

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            return Response(
                {
                    'error': 'Product not found'
                },
                status=404
            )

        if quantity <= 0:

            return Response(
                {
                    'error': 'Quantity must be greater than 0'
                },
                status=400
            )

        if quantity > product.stock:

            return Response(
                {
                    'error': 'Not enough stock'
                },
                status=400
            )

        now = timezone.now()

        cart, created = Cart.objects.get_or_create(
            user=request.user,
            defaults={
                'expires_at':
                now + timedelta(hours=2)
            }
        )

        if cart.expires_at <= now:

            cart.items.all().delete()

            cart.created_at = now

            cart.expires_at = (
                now + timedelta(hours=2)
            )

            cart.save()

        item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if item_created:

            item.quantity = quantity

        else:

            item.quantity += quantity

        if item.quantity > product.stock:

            return Response(
                {
                    'error': 'Not enough stock'
                },
                status=400
            )

        item.save()

        return Response(
            CartSerializer(cart).data,
            status=201
        )


class CartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        now = timezone.now()

        try:

            cart = Cart.objects.get(
                user=request.user
            )

        except Cart.DoesNotExist:

            return Response({
                'message': 'Cart is empty'
            })

        if cart.expires_at <= now:

            cart.items.all().delete()

            return Response({
                'message': 'Cart expired',
                'items': []
            })

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )


class RemoveCartItemView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):

        try:

            item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )

        except CartItem.DoesNotExist:

            return Response(
                {
                    'error': 'Cart item not found'
                },
                status=404
            )

        item.delete()

        return Response({
            'message': 'Item removed successfully'
        })


class UpdateCartItemView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):

        try:

            quantity = int(
                request.data.get(
                    'quantity',
                    1
                )
            )

        except (TypeError, ValueError):

            return Response(
                {
                    'error': 'Invalid quantity'
                },
                status=400
            )

        if quantity <= 0:

            return Response(
                {
                    'error':
                    'Quantity must be greater than 0'
                },
                status=400
            )

        try:

            item = CartItem.objects.get(
                id=item_id,
                cart__user=request.user
            )

        except CartItem.DoesNotExist:

            return Response(
                {
                    'error':
                    'Cart item not found'
                },
                status=404
            )

        if quantity > item.product.stock:

            return Response(
                {
                    'error': 'Not enough stock'
                },
                status=400
            )

        item.quantity = quantity

        item.save()

        return Response({
            'message':
            'Quantity updated successfully',

            'quantity':
            item.quantity
        })