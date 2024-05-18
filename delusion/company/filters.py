import django_filters
from .models import Company


class CompanyFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(
        field_name='created_at', input_formats=["%Y-%m-%d"]
    )
    created_at__gte = django_filters.DateFilter(
        field_name='created_at', lookup_expr='gte', input_formats=["%Y-%m-%d"]
    )
    created_at__lte = django_filters.DateFilter(
        field_name='created_at', lookup_expr='lte', input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = Company
        fields = {
            'name': ['exact', 'icontains'],
            'parent_company': ['exact'],
        }
