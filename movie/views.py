from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework.response import Response
from movie.serializers import MovieListSerializer, GenreListSerializer, MovieValidateSerializer, \
    MovieDetailValidateSerializer, RegisterValidateSerializer
from .models import Movie, Genre
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from movie.permissions import IsSuperUser


@api_view(['GET'])
def get_data(request):
    context = {
        'number': 1,
        'text': 'ogo go',
        'bool': True,
        'list': [1, 2, 3]
    }
    return Response(data=context)


@api_view(["GET", 'POST'])
@permission_classes([IsSuperUser])
def movie_list_view(request):
    print(request.user)
    if request.method == 'GET':
        movies = Movie.objects.all()
        data = MovieListSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        print(request.data)
        serializer = MovieValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data['title']
        description = request.data['description']
        cinema_id = request.data['cinema_id']
        movie = Movie.objects.create(
            title=title,
            description=description,
            cinema_id=cinema_id,
            user=request.user
        )
        movie.genres.set(request.data['genres'])
        movie.save()
        return Response(data={'message': 'OK'})


@api_view(['GET', 'PUT', 'DELETE'])
def movie_item_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = MovieListSerializer(movie).data
        return Response(data=data)
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data={'message': 'Movie Deleted'})
    else:
        serializer = MovieDetailValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = request.data['title']
        description = request.data['description']
        cinema_id = request.data['cinema_id']
        genres = request.data['genres']
        movie.title = title
        movie.description = description
        movie.cinema_id = cinema_id
        movie.genres.set(genres)
        movie.save()
        return Response(data=MovieListSerializer(movie).data)


@api_view(['GET'])
def genres_view(request):
    genres = Genre.objects.all()

    data = GenreListSerializer(genres, many=True).data

    return Response(data=data)


@api_view(['POST'])
def login(request):
    if request.method == "POST":
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(data={"error": "User not found!"},
                            status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = RegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={'errors': serializer.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            username = request.data['username']
            password = request.data['password']
            User.objects.create_user(username=username, password=password,
                                     is_active=False)
            return Response(data={"message": "User created"})
