from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django_filters import FilterSet, NumberFilter
from rest_framework import filters as rest_filters
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.showbill.serializers import AdvertModelSerializer, CarModelSerializer
from showbill.models import Advert, Car
# from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger(__name__)


class AdvertFilter(FilterSet):
    min_price = NumberFilter(field_name="price", lookup_expr="gte")
    max_price = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Advert
        fields = ["price"]


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cars to be viewed.
    """

    queryset = Car.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = []


class AdvertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows adverts to be viewed.
    """
    queryset = Advert.objects.all()
    serializer_class = AdvertModelSerializer
    logger.info(f"Serializer: {serializer_class}")

    logger.info(f"Queryset: {queryset}")
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


"""
class CombineListView(viewsets.GenericViewSet):
    serializer_class_Car = CarModelSerializer
    serializer_class_Advert = AdvertModelSerializer

    def get_queryset_Cars(self):
        return Car.objects.all()

    def get_queryset_Adverts(self):
        return Advert.objects.all()

    def list(self, request, *args, **kwargs):
        car = self.serializer_class_Car(self.get_queryset_Cars(), many=True)
        advert = self.serializer_class_Advert(self.get_queryset_Adverts(), many=True)
        return Response({
            "Adverts": advert.data["car": car.data]
        })
"""