from rest_framework.pagination import PageNumberPagination


class ProductsPageNumberPagination(PageNumberPagination):
    page_size = 21