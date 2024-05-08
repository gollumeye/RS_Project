from django.db import models
from django.contrib.postgres.fields import ArrayField

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    genres = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    title = models.CharField(max_length=255)
    release_year = models.CharField(max_length=4, blank=True, null=True)
    tags_ids = ArrayField(models.IntegerField(), blank=True, null=True)
    actors = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    production_companies = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    adult = models.BooleanField(default=False)
    writers = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    directors = ArrayField(models.CharField(max_length=255), blank=True, null=True)

class Rating(models.Model):
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        unique_together = ('user_id', 'movie_id')

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name
