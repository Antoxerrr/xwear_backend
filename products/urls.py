from django.urls import path
from rest_framework.routers import SimpleRouter

from products.views import ProductsViewSet, filters_data_view

router = SimpleRouter()
router.register('(?P<chapter_slug>[-\w]+)', ProductsViewSet, basename='products')

urlpatterns = router.urls + [
    path('filters_data/', filters_data_view, name='filters_data'),
]
