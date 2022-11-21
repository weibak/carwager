from rest_framework import serializers

from news.models import News


class NewsModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ["id", "title", "image", "slug", "text", "created_at"]
