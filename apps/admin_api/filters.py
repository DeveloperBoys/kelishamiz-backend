import django_filters

from apps.users.models import User
from apps.classifieds.models import Classified


class UserFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = User
        fields = ['is_active',]


class ClassifiedFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Classified
        fields = ['status',]
