from datetime import timedelta

from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth, TruncWeek
from django.utils import timezone
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.filters import FinancialRecordFilter, UserFilter
from core.models import FinancialRecord, Role, User
from core.serializers import (
    FinancialRecordsSerializer,
    RoleSerializer,
    UserSerializer,
)
from dashboard.permissions import (
    FinancialRecordPermission,
    IsAdmin,
    SummaryPermission,
)


class UserManagementViewSet(ModelViewSet):
    queryset = User.objects.select_related("role").all().order_by("id")
    permission_classes = [IsAdmin]
    serializer_class = UserSerializer
    filterset_class = UserFilter

    @action(methods=["patch"], detail=True, url_path="toggle")
    def toggle_activity(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"message": "Successfully toggled user status", "is_active": user.is_active})


class RecordsViewSet(ModelViewSet):
    queryset = FinancialRecord.objects.select_related("user").all().order_by("-date", "-id")
    permission_classes = [FinancialRecordPermission]
    serializer_class = FinancialRecordsSerializer
    filterset_class = FinancialRecordFilter


class RoleManagementViewSet(ModelViewSet):
    queryset = Role.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = RoleSerializer


@api_view(["GET"])
@permission_classes([SummaryPermission])
def total_income(request):
    total = (FinancialRecord.objects.filter(record_type="income").aggregate(total=Sum("amount"))["total"] or 0)
    return Response({"total_income": total})


@api_view(["GET"])
@permission_classes([SummaryPermission])
def total_expense(request):
    total = (FinancialRecord.objects.filter(record_type="expense").aggregate(total=Sum("amount"))["total"] or 0)
    return Response({"total_expense": total})


@api_view(["GET"])
@permission_classes([SummaryPermission])
def net_balance(request):
    total_income_amount = (FinancialRecord.objects.filter(record_type="income").aggregate(total=Sum("amount"))["total"] or 0)
    total_expense_amount = (FinancialRecord.objects.filter(record_type="expense").aggregate(total=Sum("amount"))["total"]or 0)

    return Response({"net_balance": total_income_amount - total_expense_amount})


@api_view(["GET"])
@permission_classes([SummaryPermission])
def category_totals(request, category):
    records = FinancialRecord.objects.filter(category__iexact=category).aggregate(
        total_income=Sum("amount", filter=Q(record_type="income")),
        total_expense=Sum("amount", filter=Q(record_type="expense")),
    )

    return Response(
        {
            "category": category,
            "total_income": records["total_income"] or 0,
            "total_expense": records["total_expense"] or 0,
            "net": (records["total_income"] or 0) - (records["total_expense"] or 0),
        }
    )


@api_view(["GET"])
@permission_classes([SummaryPermission])
def recent_activity(request):
    records = FinancialRecord.objects.filter(created_at__gte=timezone.now() - timedelta(days=3)).order_by("-created_at")
    serializer = FinancialRecordsSerializer(records, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([SummaryPermission])
def trends(request):
    group = request.query_params.get("group", "monthly").lower()
    trunc_map = {
        "weekly": TruncWeek,
        "monthly": TruncMonth,
    }

    if group not in trunc_map:
        return Response(
            {"detail": "Invalid group. Use 'weekly' or 'monthly'."},
            status=400,
        )

    points = (
        FinancialRecord.objects.annotate(period=trunc_map[group]("date"))
        .values("period")
        .annotate(
            total_income=Sum("amount", filter=Q(record_type="income")),
            total_expense=Sum("amount", filter=Q(record_type="expense")),
        )
        .order_by("period")
    )

    response_points = []
    for point in points:
        total_income_amount = point["total_income"] or 0
        total_expense_amount = point["total_expense"] or 0
        period = point["period"]

        response_points.append(
            {
                "label": period.strftime("%Y-%m-%d")
                if group == "weekly"
                else period.strftime("%Y-%m"),
                "period_start": period.date().isoformat(),
                "total_income": total_income_amount,
                "total_expense": total_expense_amount,
                "net_balance": total_income_amount - total_expense_amount,
            }
        )

    return Response({"group": group, "points": response_points})
