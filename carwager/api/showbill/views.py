from rest_framework import viewsets


from api.showbill.serializers import AdvertModelSerializer
from showbill.models import Advert
from rest_framework.permissions import IsAuthenticated


class AdvertViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows adverts to be viewed.
    """

    queryset = Advert.objects.all().order_by("-created_at")
    serializer_class = AdvertModelSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
