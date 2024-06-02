from movieRecommenderApp.models import Movie
from movieRecommenderApp.recommendationAlgorithms.popularMoviesOfSameYear import recommend_popular_movies_of_same_year

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


"""
Recommends movies were similar persons where involved as in the selected movie. The following features attribute to this with the following weights:
 - actors: 50%
 - directors: 20%
 - writers: 20%
 - production companies: 10%
 
uses jaccard similarity
"""
def recommend_movies_with_similar_persons_involved(movie):
    movies = Movie.objects.exclude(pk=movie.pk) \
        .exclude(actors__isnull=True) \
        .exclude(directors__isnull=True) \
        .exclude(writers__isnull=True) \
        .exclude(production_companies__isnull=True)

    if not movie.adult:
        movies = movies.filter(adult=False)

    actors = set(movie.actors) if movie.actors else set()
    directors = set(movie.directors) if movie.directors else set()
    writers = set(movie.writers) if movie.writers else set()
    production_companies = set(movie.production_companies) if movie.production_companies else set()

    if not actors and not directors and not writers and not production_companies:
        return recommend_popular_movies_of_same_year(movie)

    similar_movies_sorted = []

    for other_movie in movies:
        other_movie_actors = set(other_movie.actors) if other_movie.actors else set()
        other_movie_directors = set(other_movie.directors) if other_movie.directors else set()
        other_movie_writers = set(other_movie.writers) if other_movie.writers else set()
        other_movie_production_companies = set(other_movie.production_companies) if other_movie.production_companies else set()

        actors_similarity = jaccard_similarity(actors, other_movie_actors)
        directors_similarity = jaccard_similarity(directors, other_movie_directors)
        writers_similarity = jaccard_similarity(writers, other_movie_writers)
        production_companies_similarity = jaccard_similarity(production_companies,other_movie_production_companies)

        combined_weighted_similarity = (0.5 * actors_similarity) + (0.2 * directors_similarity) + (0.2 * writers_similarity) + (0.1 * production_companies_similarity)
        similar_movies_sorted.append((other_movie, combined_weighted_similarity))

    similar_movies_sorted = sorted(similar_movies_sorted, key=lambda x: x[1], reverse=True)[:5]
    similar_movies = [movie for movie, _ in similar_movies_sorted]

    return similar_movies