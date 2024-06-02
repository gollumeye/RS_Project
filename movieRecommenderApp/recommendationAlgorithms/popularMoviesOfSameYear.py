from movieRecommenderApp.models import Movie

"""
From movies released in the same year as the selected one, returns most popular and best voted movies.
This algorithm is very unspecific for recommendations, but is used as a fallback algorithm for some of our other algorithms, if the required information for those is not provided by the selected movie
"""
def recommend_popular_movies_of_same_year(movie):
    movies_same_year = Movie.objects.filter(release_year=movie.release_year).exclude(pk=movie.pk)

    if not movie.adult:
        movies_same_year = movies_same_year.filter(adult=False)

    movies_same_year = movies_same_year.exclude(popularity__isnull=True).exclude(vote_average__isnull=True)

    sorted_movies = movies_same_year.order_by('-popularity', '-vote_average')
    similar_movies = sorted_movies[:5]
    return similar_movies