from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=100
    )

    stock = models.IntegerField(
        default=0
    )

    def __str__(self):

        return self.name


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'user',
            'product'
        )

    def __str__(self):

        return f"{self.user.username} - {self.product.name}"


class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        unique_together = (
            'product',
            'user'
        )

    def __str__(self):

        return f"{self.product.name} - {self.rating}"