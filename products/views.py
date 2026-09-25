from rest_framework import viewsets
from rest_framework import status

from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)

from rest_framework.pagination import PageNumberPagination

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import (
    Product,
    Wishlist,
    Review
)

from .serializers import (
    ProductSerializer,
    WishlistSerializer,
    ReviewSerializer
)


# =====================================================
# PRODUCT PAGINATION
# =====================================================

class ProductPagination(PageNumberPagination):

    page_size = 20

    page_size_query_param = 'page_size'

    max_page_size = 1000


# =====================================================
# PRODUCT VIEWSET
# =====================================================

class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    pagination_class = ProductPagination

    def get_queryset(self):

        products = Product.objects.all()

        # -----------------------------
        # SEARCH
        # -----------------------------

        search = self.request.query_params.get(
            'search'
        )

        if search:

            products = products.filter(
                name__icontains=search
            ) | products.filter(
                description__icontains=search
            ) | products.filter(
                category__icontains=search
            )

        # -----------------------------
        # CATEGORY
        # -----------------------------

        category = self.request.query_params.get(
            'category'
        )

        if category and category != 'All':

            products = products.filter(
                category__iexact=category
            )

        # -----------------------------
        # MINIMUM PRICE
        # -----------------------------

        price_min = self.request.query_params.get(
            'price_min'
        )

        if price_min:

            products = products.filter(
                price__gte=price_min
            )

        # -----------------------------
        # MAXIMUM PRICE
        # -----------------------------

        price_max = self.request.query_params.get(
            'price_max'
        )

        if price_max:

            products = products.filter(
                price__lte=price_max
            )

        # -----------------------------
        # SORT
        # -----------------------------

        sort = self.request.query_params.get(
            'sort'
        )

        if sort == 'low':

            products = products.order_by(
                'price'
            )

        elif sort == 'high':

            products = products.order_by(
                '-price'
            )

        else:

            products = products.order_by(
                'id'
            )

        return products

    # -----------------------------
    # PERMISSIONS
    # -----------------------------

    def get_permissions(self):

        if self.request.method in [
            'GET',
            'HEAD',
            'OPTIONS'
        ]:

            return [AllowAny()]

        return [IsAdminUser()]


# =====================================================
# WISHLIST
# =====================================================

class WishlistView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        wishlist = Wishlist.objects.filter(
            user=request.user
        ).order_by('-created_at')

        serializer = WishlistSerializer(
            wishlist,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        product_id = request.data.get(
            'product_id'
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

        wishlist, created = Wishlist.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:

            return Response({
                'message': 'Already in wishlist'
            })

        return Response(
            {
                'message': 'Added to wishlist'
            },
            status=201
        )

    def delete(self, request, product_id):

        try:

            wishlist = Wishlist.objects.get(
                user=request.user,
                product_id=product_id
            )

        except Wishlist.DoesNotExist:

            return Response(
                {
                    'error': 'Wishlist item not found'
                },
                status=404
            )

        wishlist.delete()

        return Response({
            'message': 'Removed from wishlist'
        })


# =====================================================
# REVIEWS
# =====================================================

class ReviewView(APIView):

    def get(self, request, product_id):

        reviews = Review.objects.filter(
            product_id=product_id
        ).order_by('-created_at')

        serializer = ReviewSerializer(
            reviews,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request, product_id):

        if not request.user.is_authenticated:

            return Response(
                {
                    'error': 'Please login first'
                },
                status=401
            )

        existing_review = Review.objects.filter(
            product_id=product_id,
            user=request.user
        ).first()

        if existing_review:

            return Response(
                {
                    'error': 'You already reviewed this product'
                },
                status=400
            )

        rating = request.data.get(
            'rating'
        )

        comment = request.data.get(
            'comment'
        )

        if not rating or not comment:

            return Response(
                {
                    'error': 'Rating and comment are required'
                },
                status=400
            )

        if int(rating) < 1 or int(rating) > 5:

            return Response(
                {
                    'error': 'Rating must be between 1 and 5'
                },
                status=400
            )

        review = Review.objects.create(
            product_id=product_id,
            user=request.user,
            rating=rating,
            comment=comment
        )

        serializer = ReviewSerializer(
            review
        )

        return Response(
            serializer.data,
            status=201
        )



















































        