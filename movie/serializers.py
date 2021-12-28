from rest_framework import serializers
from movie.models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cinema', ]
