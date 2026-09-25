from django.db import models

from django.contrib.auth.models import User


class Order(models.Model):

    STATUS_CHOICES = [

        ('Pending', 'Pending'),

        ('Confirmed', 'Confirmed'),

        ('Shipped', 'Shipped'),

        ('Delivered', 'Delivered'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_method = models.CharField(
        max_length=30,
        default='COD'
    )

    payment_status = models.CharField(
        max_length=30,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        if self.product:

            return self.product.name

        return "Deleted Product"