import django_filters
from django.db.models import Q

from core.models import FinancialRecord, User


class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_search")
    role = django_filters.CharFilter(field_name="role__name", lookup_expr="iexact")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ["search", "role", "is_active"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value)
            | Q(first_name__icontains=value)
            | Q(last_name__icontains=value)
        )


class FinancialRecordFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category", lookup_expr="iexact")
    record_type = django_filters.CharFilter(field_name="record_type", lookup_expr="iexact")
    user_id = django_filters.NumberFilter(field_name="user_id")
    search = django_filters.CharFilter(method="filter_search")
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="date__gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="date__lte")
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = FinancialRecord
        fields = [
            "category",
            "record_type",
            "user_id",
            "search",
            "date_from",
            "date_to",
            "amount_min",
            "amount_max",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(notes__icontains=value)
