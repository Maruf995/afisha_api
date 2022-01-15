from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from movie.models import Movie, Review
from rest_framework import serializers
from movie.models import Movie, Genre, Cinema
from django.contrib.auth.models import User


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text']


class MovieListSerializer(serializers.ModelSerializer):
    cinema = serializers.SerializerMethodField(source='get_cinema')
    genres = serializers.SerializerMethodField(source='get_genres')
    reviews = serializers.SerializerMethodField(source='get_reviews')

    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['id', 'user', 'title', 'description', 'cinema', 'genres', 'reviews']

    def get_cinema(self, obj):
        return obj.cinema.name

    def get_genres(self, obj):
        return GenreListSerializer(obj.genres, many=True).data

    def get_reviews(self, obj):
        return ReviewListSerializer(obj.reviews, many=True).data


class MovieValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=50)
    description = serializers.CharField(max_length=200, required=False)
    cinema_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_title(self, title):
        movies = Movie.objects.filter(title=title)
        if movies.count() > 0:
            raise ValidationError('Movie with this name already exists!')

    def validate_cinema_id(self, cinema_id):
        try:
            Cinema.objects.get(id=cinema_id)
        except Cinema.DoesNotExist:
            raise ValidationError("cinema_id not found!")

    def validate(self, attrs):
        cinema_id = attrs['cinema_id']
        try:
            Cinema.objects.get(id=cinema_id)
        except Cinema.DoesNotExist:
            raise ValidationError("cinema_id not found")


class MovieDetailValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=50)
    description = serializers.CharField(max_length=200, required=False)
    cinema_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())


class RegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=2, max_length=10)

    def validate_username(self, username):
        users = User.objects.filter(username=username)
        if users.count() > 0:
            raise ValidationError('User with this name already exists!')
