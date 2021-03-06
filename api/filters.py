from django_filters import rest_framework as filters

from api.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(
        field_name='genre__slug',
    )
    category = filters.CharFilter(
        field_name='category__slug',
    )
    year = filters.NumberFilter(
        field_name='year',
    )
    name = filters.CharFilter(
        lookup_expr="contains",
    )

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
