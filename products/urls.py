from django.urls import path

from .views import (
    WishlistView,
    ReviewView
)


urlpatterns = [

    path(
        'wishlist/',
        WishlistView.as_view()
    ),

    path(
        'wishlist/<int:product_id>/',
        WishlistView.as_view()
    ),

    path(
        '<int:product_id>/reviews/',
        ReviewView.as_view()
    ),
]