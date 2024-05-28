from movieRecommenderApp.models import Movie


def recommend_movies_with_similar_persons_involved(movie):
    movies_query = Movie.objects.exclude(pk=movie.id)
    movies = movies_query

    #TODO

    similar_movies = []

    return similar_movies