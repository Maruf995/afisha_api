from django.contrib import admin
from movie.models import Cinema, Movie, Genre, Review
# Register your models here.

admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Review)