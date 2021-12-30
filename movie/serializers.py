from rest_framework import serializers
from movie.models import Movie, Review, Genre, Cinema


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text'.split()


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'id name'.split()

class MovieListSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = 'id title description cinema genres reviews'.split()

    def get_reviews(self, obj):
        return ReviewListSerializer(obj.reviews, many=True).data

    def get_genres(self, obj):
        return GenreListSerializer(obj.genres, many=True).data

