from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, get_object_or_404
from .models import Movie, Tag


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
    tags = Tag.objects.filter(tag_id__in=movie.tags_ids)
    return render(request, 'recommendations_page.html', {'movie': movie, 'tags': tags})