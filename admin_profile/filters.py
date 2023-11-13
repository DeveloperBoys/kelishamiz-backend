import django_filters

from apps.users.models import User


class UserFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name="is_active")

    class Meta:
        model = User
        fields = ['is_active',]
