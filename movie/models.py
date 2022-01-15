from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


from django.contrib.auth.models import User


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)
    reviews = models.ManyToManyField(Review, related_name='reviews')

    def __str__(self):
        return self.title
