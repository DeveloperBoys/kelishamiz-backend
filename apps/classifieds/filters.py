import django_filters

from .models import Classified, Category
from apps.site_settings.models import Locations


class ClassifiedFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="classifieddetail__price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(
        field_name="classifieddetail__price", lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all())
    location = django_filters.ModelChoiceFilter(
        queryset=Locations.objects.all()
    )

    class Meta:
        model = Classified
        fields = ['min_price', 'max_price', 'category', 'location']
