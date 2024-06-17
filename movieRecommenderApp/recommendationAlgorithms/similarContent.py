from movieRecommenderApp.models import Movie, Tag
from movieRecommenderApp.recommendationAlgorithms.popularMoviesOfSameYear import recommend_popular_movies_of_same_year

def dice_coefficient(set1, set2):
    intersection = len(set1.intersection(set2))
    dice = 2 * intersection / (len(set1) + len(set2))
    return dice

"""
Recommends similar movies based on the content, based on 
- genre overlap
- tags overlap
(both weigh equally much)

uses dice coefficient as similarity measure
"""
def recommend_movies_with_similar_content(movie):
    movies = Movie.objects.exclude(pk=movie.id) \
        .exclude(genres__isnull=True) \
        .exclude(genres__exact='{}') \
        .exclude(tags_ids__isnull=True) \
        .exclude(tags_ids__exact='{}')

    if not movie.adult:
        movies = movies.filter(adult=False)

    chosen_movie_genres = set(movie.genres) if movie.genres else set()
    chosen_movie_tags_ids = set(movie.tags_ids) if movie.tags_ids else set()
    if len(chosen_movie_genres) == 0 and len(chosen_movie_tags_ids) == 0: #cannot recommend if chosen movie has no genres or tags
        return recommend_popular_movies_of_same_year(movie) #fallback recommendation algorithm

    similar_movies = []

    for movie in movies:
        movie_genres = set(movie.genres) if movie.genres else set()
        movie_tags_ids = set(movie.tags_ids) if movie.tags_ids else set()

        genre_similarity = dice_coefficient(chosen_movie_genres, movie_genres)
        tag_similarity = dice_coefficient(chosen_movie_tags_ids, movie_tags_ids)

        combined_similarity = (genre_similarity + tag_similarity) / 2 #equal weight for genres and tags
        similar_movies.append((movie, combined_similarity))

    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[:5] #sort and take top 5
    similar_movies = [movie for movie, score in similar_movies]

    return similar_movies
