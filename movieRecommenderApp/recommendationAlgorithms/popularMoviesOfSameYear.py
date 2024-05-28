from movieRecommenderApp.models import Movie


def recommend_popular_movie_of_same_year(movie):
    movies_query = Movie.objects.exclude(pk=movie.id)
    movies = movies_query

    #TODO

    similar_movies = []

    return similar_movies