from rest_framework import viewsets


from api.auction.serializers import AuctionModelSerializer
from auction.models import Auction
from rest_framework.permissions import IsAuthenticated


class AuctionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows auctions to be viewed.
    """

    queryset = Auction.objects.all().order_by("-created_at")
    serializer_class = AuctionModelSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
