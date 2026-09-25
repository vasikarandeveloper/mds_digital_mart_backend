from django.db import transaction
from django.db.models import Sum

from django.utils import timezone

from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.response import Response

from rest_framework.views import APIView

from cart.models import Cart

from products.models import Product

from .models import (
    Order,
    OrderItem
)

from .serializers import OrderSerializer


class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):

        address = request.data.get(
            'address',
            ''
        ).strip()

        payment_method = request.data.get(
            'payment_method',
            'COD'
        )

        if not address:

            return Response(
                {
                    'error':
                    'Address is required'
                },
                status=400
            )

        if payment_method != 'COD':

            return Response(
                {
                    'error':
                    'Invalid payment method'
                },
                status=400
            )

        try:

            cart = Cart.objects.get(
                user=request.user
            )

        except Cart.DoesNotExist:

            return Response(
                {
                    'error':
                    'Cart is empty'
                },
                status=400
            )

        items = cart.items.select_related(
            'product'
        ).all()

        if not items.exists():

            return Response(
                {
                    'error':
                    'Cart is empty'
                },
                status=400
            )

        if cart.expires_at <= timezone.now():

            cart.items.all().delete()

            return Response(
                {
                    'error':
                    'Cart expired'
                },
                status=400
            )

        subtotal = 0

        for item in items:

            if item.quantity > item.product.stock:

                return Response(
                    {
                        'error':
                        f'Not enough stock for {item.product.name}'
                    },
                    status=400
                )

            subtotal += (
                item.product.price *
                item.quantity
            )

        if subtotal >= 500:

            delivery_fee = 0

        else:

            delivery_fee = 40

        total_amount = (
            subtotal +
            delivery_fee
        )

        order = Order.objects.create(
            user=request.user,

            total_amount=total_amount,

            address=address,

            payment_method=payment_method,

            payment_status='Pending'
        )

        for item in items:

            OrderItem.objects.create(
                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price
            )

            item.product.stock -= (
                item.quantity
            )

            item.product.save()

        cart.items.all().delete()

        serializer = OrderSerializer(
            order
        )

        return Response(
            {
                'message':
                'Order placed successfully',

                'order': serializer.data,

                'subtotal': subtotal,

                'delivery_fee':
                delivery_fee,

                'total_amount':
                total_amount
            },
            status=201
        )


class OrderHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.filter(
            user=request.user
        ).prefetch_related(
            'items__product'
        ).order_by(
            '-created_at'
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data
        )


class OrderStatusUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):

        try:

            order = Order.objects.get(
                id=order_id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error':
                    'Order not found'
                },
                status=404
            )

        status_value = request.data.get(
            'status'
        )

        valid_status = [
            'Pending',
            'Confirmed',
            'Shipped',
            'Delivered'
        ]

        if status_value not in valid_status:

            return Response(
                {
                    'error':
                    'Invalid status'
                },
                status=400
            )

        order.status = status_value

        order.save()

        return Response({
            'message':
            'Order status updated successfully',

            'status':
            order.status
        })


class PaymentStatusUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):

        try:

            order = Order.objects.get(
                id=order_id
            )

        except Order.DoesNotExist:

            return Response(
                {
                    'error':
                    'Order not found'
                },
                status=404
            )

        payment_status = request.data.get(
            'payment_status'
        )

        valid_status = [
            'Pending',
            'Paid',
            'Failed'
        ]

        if payment_status not in valid_status:

            return Response(
                {
                    'error':
                    'Invalid payment status'
                },
                status=400
            )

        order.payment_status = (
            payment_status
        )

        order.save()

        return Response({
            'message':
            'Payment status updated successfully',

            'payment_status':
            order.payment_status
        })


class AdminDashboardView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_products = (
            Product.objects.count()
        )

        total_orders = (
            Order.objects.count()
        )

        pending_orders = (
            Order.objects.filter(
                status='Pending'
            ).count()
        )

        total_revenue = (
            Order.objects.aggregate(
                total=Sum('total_amount')
            )['total'] or 0
        )

        paid_orders = (
            Order.objects.filter(
                payment_status='Paid'
            ).count()
        )

        pending_payments = (
            Order.objects.filter(
                payment_status='Pending'
            ).count()
        )

        return Response({

            'total_products':
            total_products,

            'total_orders':
            total_orders,

            'pending_orders':
            pending_orders,

            'total_revenue':
            total_revenue,

            'paid_orders':
            paid_orders,

            'pending_payments':
            pending_payments
        })


class AdminOrderListView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = Order.objects.all().prefetch_related(
            'items__product'
        ).order_by(
            '-created_at'
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data
        )