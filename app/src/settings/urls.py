from django.conf import settings
from django.shortcuts import render
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers


def error_404(request, exception):
    return render(request, "error/404.html", status=404)


def error_500(request):
    return render(request, "error/500.html", status=500)


handler404 = "src.settings.urls.error_404"
handler500 = "src.settings.urls.error_500"


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=True):
        schema = super().get_schema(request, public)
        schema.schemes = settings.REST_FRAMEWORK_SCHEMAS
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="CryptoTrendAnalyzer",
        default_version="v1",
        description="API RESTful utilizando o Django Rest Framework (DRF) e PostgreSQL, focada na entrega de análises de médias móveis simples (MMS) para os pares de criptomoedas Bitcoin (BRLBTC) e Ethereum (BRLETH), conforme listados no Mercado Bitcoin. As médias móveis são calculadas para os períodos de 20, 50 e 200 dias.",
        terms_of_service="https://github.com/alexiusstrauss/CryptoTrendAnalyzer/blob/main/LICENSE",
        contact=openapi.Contact(email="alexius.dev@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

router = routers.SimpleRouter()

urlpatterns = [
    path("api/", include("src.apps.system.api.v1.urls")),
    path('market_trends/', include('src.apps.market_trends.api.urls')),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
