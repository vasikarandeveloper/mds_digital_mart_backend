from django.db import models

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name

class Product(models.Model):

    name = models.CharField(max_length=150)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    description = models.TextField()
    stock = models.IntegerField(default=0)
    Category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'pending'),
            ('processing', 'processing'),
            ('shipped', 'shipped'),
            ('delivered', 'delivered'),
            ('cancelled', 'cancelled'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)