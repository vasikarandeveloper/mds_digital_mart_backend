from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):

    help = "Create 500 sample products"

    def handle(self, *args, **kwargs):

        products = []

        product_types = {
            "Mobiles": [
                "Smartphone",
                "5G Smartphone",
                "Android Phone",
                "Gaming Phone",
                "Camera Phone"
            ],

            "Electronics": [
                "Laptop",
                "Smart TV",
                "Monitor",
                "Keyboard",
                "Mouse",
                "Tablet",
                "Printer"
            ],

            "Fashion": [
                "Men T-Shirt",
                "Men Shirt",
                "Women Dress",
                "Jeans",
                "Jacket",
                "Sneakers",
                "Saree"
            ],

            "Home": [
                "Office Chair",
                "Study Table",
                "Bedsheet",
                "Pillow",
                "Curtain",
                "Storage Box"
            ],

            "Accessories": [
                "Wireless Earbuds",
                "Bluetooth Headphones",
                "Smart Watch",
                "Power Bank",
                "USB Cable",
                "Mobile Cover"
            ],

            "Beauty": [
                "Face Wash",
                "Moisturizer",
                "Shampoo",
                "Body Lotion",
                "Perfume"
            ],

            "Toys": [
                "Remote Car",
                "Building Blocks",
                "Puzzle",
                "Doll",
                "Board Game"
            ],

            "Sports": [
                "Cricket Bat",
                "Football",
                "Badminton Racket",
                "Yoga Mat",
                "Sports Shoes"
            ],

            "Books": [
                "Python Programming Book",
                "JavaScript Book",
                "Web Development Book",
                "Database Book",
                "Novel",
                "Exam Preparation Book"
            ]
        }

        number = 1

        while number <= 500:

            for category, types in product_types.items():

                for product_type in types:

                    if number > 500:
                        break

                    product_name = (
                        f"{product_type} "
                        f"Model {number}"
                    )

                    price = 499 + (
                        (number * 137) % 50000
                    )

                    stock = 10 + (
                        number % 91
                    )

                    products.append(
                        Product(
                            name=product_name,
                            description=(
                                f"High quality {product_type} "
                                f"available at MDS DigitalMart."
                            ),
                            price=price,
                            category=category,
                            stock=stock
                        )
                    )

                    number += 1

                if number > 500:
                    break

        Product.objects.bulk_create(
            products,
            ignore_conflicts=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                "500 products created successfully!"
            )
        )