from django_filters import rest_framework as filters
from django_filters import FilterSet#, DateFilter

from advertisements.models import Advertisement

class AdvertisementFilter(FilterSet):
    created_at = filters.DateFromToRangeFilter()
    # created_min = filters.DateFilter(field_name="created_at", lookup_expr='gte')
    # created_max = filters.DateFilter(field_name="created_at", lookup_expr='lte')
    class Meta:
        model = Advertisement
        fields = ["status", "created_at"]
