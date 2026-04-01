from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenRefreshView

from dashboard.auth import CustomTokenObtainView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", CustomTokenObtainView.as_view(), name="token-obtain"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("core.urls")),
]
