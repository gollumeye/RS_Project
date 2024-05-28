from movieRecommenderApp.models import Movie, Tag

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def recommend_movies_with_similar_content(movie):
    movies = Movie.objects.exclude(pk=movie.id) \
        .exclude(genres__isnull=True) \
        .exclude(genres__exact='{}') \
        .exclude(tags_ids__isnull=True) \
        .exclude(tags_ids__exact='{}')

    chosen_movie_genres = set(movie.genres) if movie.genres else set()
    chosen_movie_tags_ids = set(movie.tags_ids) if movie.tags_ids else set()
    if len(chosen_movie_genres) is 0 and len(chosen_movie_tags_ids) is 0: #cannot recommend if chosen movie has no genres or tags
        return []

    similar_movies = []

    for movie in movies:
        movie_genres = set(movie.genres) if movie.genres else set()
        movie_tags_ids = set(movie.tags_ids) if movie.tags_ids else set()

        genre_similarity = jaccard_similarity(chosen_movie_genres, movie_genres)
        tag_similarity = jaccard_similarity(chosen_movie_tags_ids, movie_tags_ids)
        combined_similarity = (genre_similarity + tag_similarity) / 2 #equal weight for genres and tags
        similar_movies.append((movie, combined_similarity))

    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[:5] #sort and take top 5
    similar_movies = [movie for movie, score in similar_movies]

    return similar_movies
