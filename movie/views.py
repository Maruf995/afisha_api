from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie.serializers import MovieListSerializer
from .models import Movie
from rest_framework import status


@api_view(['GET'])
def get_data(request):
    context = {
        'number': 1,
        'text': 'ogo go',
        'bool': True,
        'list': [1, 2, 3]
    }
    return Response(data=context)


@api_view(["GET"])
def movie_list_view(request):
    movies = Movie.objects.all()
    data = MovieListSerializer(movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_detail_view(request, id):
    try:
        movie = Movie.objects.get(id=id)
    except Movie.DoesNotExist:
        return Response(data={'message': 'Product not found'},
                        status=status.HTTP_404_NOT_FOUND)
    data = MovieListSerializer(movie).data
    return Response(data=data)
