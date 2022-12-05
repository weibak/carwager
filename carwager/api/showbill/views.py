from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django_filters import FilterSet, NumberFilter
from rest_framework import filters as rest_filters
from api.showbill.serializers import AdvertModelSerializer
from showbill.models import Advert, Car
# from rest_framework.permissions import IsAuthenticated


class AdvertFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Advert
        fields = ["price"]


class AdvertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows adverts to be viewed.
    """
    serializer_class = AdvertModelSerializer
    queryset = Advert.objects.all()
    filter_backends = [
        rest_filters.SearchFilter,
        rest_filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = AdvertFilter
    search_fields = ["price", "car"]
    ordering_fields = ["car", "price"]

    def get_queryset(self):
        queryset = Advert.objects.all()
        mark = self.request.query_params.get("mark")
        if mark is not None:
            queryset = queryset.filter(car__mark__car_mark=mark)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


