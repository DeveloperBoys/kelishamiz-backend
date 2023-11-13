from rest_framework import serializers
from .models import SearchQuery


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = ('id', 'user', 'query', 'timestamp')
        read_only_fields = ('id', 'timestamp')
