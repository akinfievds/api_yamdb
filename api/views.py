from rest_framework import filters, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Genre, Category, Title
from .serializers import (
    GenreSerializer, CategorySerializer, TitleSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'year', 'genre', 'category' ]
