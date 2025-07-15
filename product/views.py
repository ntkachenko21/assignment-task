from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from product.models import Product
from product.serializers import ProductSerializer, ProductCreateSerializer
from product.filters import ProductFilter


@extend_schema(
    tags=["Products"],
)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductSerializer
        return ProductCreateSerializer

    @extend_schema(
        summary="List all products",
        description="Returns a list of all products. Supports filtering by category title using `?category=Apparel`.",
        parameters=[
            OpenApiParameter(
                name="category",
                description="Filter products by category title (case insensitive exact match).",
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            )
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single product",
        description="Returns detailed information about a product by its ID.",
        responses={200: ProductSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new product",
        description="Creates a new product. Requires all product fields, including category id.",
        request=ProductCreateSerializer,
        responses={
            201: ProductSerializer,
            400: OpenApiResponse(description="Invalid input data"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
