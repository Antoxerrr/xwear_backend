from django.db.models import Prefetch, Min, Max
from drf_spectacular.utils import extend_schema
from keyring.backends.libsecret import available
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from products.models import Product, Price, Chapter, Category, Brand, ProductModel, ProductColor, Size
from products.pagination import ProductsPageNumberPagination
from products.serializers import ProductSerializer, ProductShortSerializer, FiltersDataRequestSerializer, \
    FiltersDataResponseSerializer


class ProductsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ProductSerializer
    pagination_class = ProductsPageNumberPagination

    def get_queryset(self):
        chapter_slug = self.kwargs.get('chapter_slug')

        queryset = (
            Product.objects
            .filter(category__chapter__slug=chapter_slug)
            .select_related('category', 'model', 'brand', 'collab', 'color')
            .prefetch_related(
                Prefetch('prices', Price.objects.select_related('size'))
            )
        )
        if self.action == 'retrieve':
            return queryset
        return queryset.annotate(min_price=Min('prices__price'))

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductShortSerializer
        return self.serializer_class


@extend_schema(
    parameters=[FiltersDataRequestSerializer],
    responses={
        status.HTTP_200_OK: FiltersDataResponseSerializer,
    }
)
@api_view(['GET'])
def filters_data_view(request):
    serializer = FiltersDataRequestSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    chapter = get_object_or_404(Chapter, slug=serializer.validated_data['selected_chapter'])
    available_categories = Category.objects.filter(chapter=chapter)

    products = Product.objects.filter(category__in=available_categories)

    available_brands = Brand.objects.filter(products__in=products)
    available_models = ProductModel.objects.filter(products__in=products)
    available_colors = ProductColor.objects.filter(products__in=products)
    available_prices = Price.objects.filter(product__in=products)
    available_sizes = Size.objects.filter(prices__in=available_prices)

    prices_range = available_prices.aggregate(min=Min('price'), max=Max('price'))

    data = {
        'available_categories': available_categories,
        'available_brands': available_brands,
        'available_models': available_models,
        'available_colors': available_colors,
        'available_sizes': available_sizes,
        'prices_range': prices_range,
    }
    return Response(FiltersDataResponseSerializer(data).data)
