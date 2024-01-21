from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="캔버스 생성",
        terms_of_service="https://www.backend.com/terms/",
        contact=openapi.Contact(email="contact@backend.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("", include('django_prometheus.urls')),
    path("admin/", admin.site.urls),
    path('api/v1/users/', include('user.urls')),
    path('api/v1/canvases/', include('canvas.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
