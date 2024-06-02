from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, get_object_or_404
from .models import Movie, Tag
from .recommendationAlgorithms.similarDescription import recommend_similar_movies_by_description
from .recommendationAlgorithms.popularMoviesOfSameYear import recommend_popular_movies_of_same_year
from .recommendationAlgorithms.similarMoviesByRatings import recommend_movies_by_ratings
from .recommendationAlgorithms.similarContent import recommend_movies_with_similar_content
from .recommendationAlgorithms.similarPersons import recommend_movies_with_similar_persons_involved


def movie_search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '')
        movie_similarity = Movie.objects.annotate(similarity=TrigramSimilarity('title', search_query))
        filtered_movies = movie_similarity.filter(similarity__gt=0.3)
        movies = filtered_movies.order_by('-similarity')[:10]
        return render(request, 'search_page.html', {'search_query': search_query, 'movies': movies})
    return render(request, 'search_page.html', {})

def recommendations(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if movie.tags_ids is None:
        movie.tags_ids = []
    tags = Tag.objects.filter(tag_id__in=movie.tags_ids)

    movies_with_similar_description = recommend_similar_movies_by_description(movie)
    movies_with_similar_content = recommend_movies_with_similar_content(movie)
    movies_with_similar_persons = recommend_movies_with_similar_persons_involved(movie)
    similar_movies_based_on_ratings = recommend_movies_by_ratings(movie)
    popular_movies_of_same_year = recommend_popular_movies_of_same_year(movie)

    return render(request, 'recommendations_page.html', {'movie': movie, 'tags': tags, 'moviesWithSimilarDescription': movies_with_similar_description, 'moviesWithSimilarContent': movies_with_similar_content, 'moviesWithSimilarPersonsInvolved': movies_with_similar_persons, 'similarMoviesByRatings': similar_movies_based_on_ratings, 'popularMoviesOfSameYear': popular_movies_of_same_year})