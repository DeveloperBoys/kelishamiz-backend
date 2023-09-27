import django_filters
from .models import Classified, Category


class ClassifiedFilter(django_filters.FilterSet):
    # title = django_filters.CharFilter(
    #     field_name='title', lookup_expr='icontains')
    min_price = django_filters.NumberFilter(
        field_name="classifieddetail__price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(
        field_name="classifieddetail__price", lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all())

    class Meta:
        model = Classified
        fields = ['min_price', 'max_price', 'category']
