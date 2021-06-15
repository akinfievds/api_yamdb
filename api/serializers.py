from rest_framework import serializers

from .models import Genre, Category, Title


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'description', 'year', 'genre', 'category')
        model = Title
