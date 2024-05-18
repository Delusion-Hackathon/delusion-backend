from django.db.models.query import QuerySet
from .models import (
    Company,
    Worker
)


def all_companies() -> QuerySet[Company]:
    return Company.objects.select_related('parent_company').filter(is_active=True)


def all_workers() -> QuerySet[Worker]:
    return Worker.objects.select_related('company', 'user').all()
