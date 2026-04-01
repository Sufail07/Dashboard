from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import (
    RoleManagementViewSet,
    UserManagementViewSet,
    RecordsViewSet,
    category_totals,
    net_balance,
    recent_activity,
    total_expense,
    total_income,
    trends,
)

router = DefaultRouter()
router.register("v1/users", UserManagementViewSet, basename="users")
router.register("v1/roles", RoleManagementViewSet, basename="roles")
router.register("v1/records", RecordsViewSet, basename="records")

urlpatterns = router.urls + [
    path("v1/summary/total-income/", total_income, name="total-income"),
    path("v1/summary/total-expense/", total_expense, name="total-expense"),
    path("v1/summary/net-balance/", net_balance, name="net-balance"),
    path("v1/summary/categories/<str:category>/", category_totals, name="category-totals"),
    path("v1/summary/recent-activity/", recent_activity, name="recent-activity"),
    path("v1/summary/trends/", trends, name="trends"),
]
