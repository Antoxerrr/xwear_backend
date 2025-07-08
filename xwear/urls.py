from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_urls = [
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
]

docs_urls = [
    path('schema/', SpectacularAPIView.as_view(), name='spectacular_schema'),
    path('', SpectacularSwaggerView.as_view(url_name='spectacular_schema'), name='swagger_ui_docs'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('docs/', include(docs_urls)),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
