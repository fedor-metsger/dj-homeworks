from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters import rest_framework as filters
from django_filters import FilterSet, DateFilter

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer

class AdvertisementFilter(FilterSet):
    created_at = filters.DateFromToRangeFilter()
    # created_min = filters.DateFilter(field_name="created_at", lookup_expr='gte')
    # created_max = filters.DateFilter(field_name="created_at", lookup_expr='lte')
    class Meta:
        model = Advertisement
        fields = ["status", "created_at"]

class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        if self.action in ["create"]:
            return [IsAuthenticated()]
        return []
