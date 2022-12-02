from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django_filters import FilterSet, NumberFilter
from rest_framework import filters as rest_filters
from api.showbill.serializers import AdvertModelSerializer
from showbill.models import Advert

# from rest_framework.permissions import IsAuthenticated

"""
class AdvertViewSet(viewsets.ModelViewSet):

    API endpoint that allows adverts to be viewed.


    queryset = Advert.objects.all().order_by("-created_at")
    serializer_class = AdvertModelSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
"""


class AdvertsListView(generics.ListAPIView):
    queryset = Advert.objects.all()
    serializer_class = AdvertModelSerializer
    filter_backends = [rest_filters.SearchFilter,
                       rest_filters.OrderingFilter,
                       DjangoFilterBackend,
                       ]
    ordering_fields = '__all__'


class AdvertsBMWListView(generics.ListAPIView):
    queryset = Advert.objects.filter(car__mark=1)
    serializer_class = AdvertModelSerializer
    filter_backends = [rest_filters.SearchFilter,
                       rest_filters.OrderingFilter,
                       DjangoFilterBackend,
                       ]
    ordering_fields = 'all'


class AdvertFilter(FilterSet):
    min_cost = NumberFilter(field_name="price", lookup_expr="gte")
    max_cost = NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Advert
        fields = ["id", "car_id", "engine_type", "engine_capacity", "drive", "gear_box", "description", "win",
                  "price", "price_usd", "phone_number", "created_at"]
