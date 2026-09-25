from django.contrib import admin

from .models import (
    Product,
    Wishlist,
    Review
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock'
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
        'category'
    )

    ordering = (
        '-id',
    )


admin.site.register(Wishlist)
admin.site.register(Review)