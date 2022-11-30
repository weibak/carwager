from rest_framework import viewsets


from api.news.serializers import NewsModelSerializer
from news.models import News
from rest_framework.permissions import IsAuthenticated


class NewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows news to be viewed.
    """

    queryset = News.objects.all().order_by("-created_at")
    serializer_class = NewsModelSerializer
    permission_classes = []
