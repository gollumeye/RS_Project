from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movieRecommenderApp.models import Movie
from movieRecommenderApp.recommendationAlgorithms.popularMoviesOfSameYear import recommend_popular_movies_of_same_year

"""
Recommends similar movies by computing the similarity between movie descriptions.
Uses TF-IDF for computing vectors for each description based on word importance
Uses cosine similarity for computing similarity between vectorized descriptions.
"""
def recommend_similar_movies_by_description(movie):

    if movie.overview is None or movie.overview == '':
        return recommend_popular_movies_of_same_year(movie) #fallback alg if no description in selected movie

    movies = Movie.objects.exclude(pk=movie.id) \
        .exclude(overview__isnull=True) \
        .exclude(overview__exact='')

    if not movie.adult:
        movies = movies.filter(adult=False)

    movie_descriptions = [mov.overview for mov in movies]
    movie_ids = [mov.pk for mov in movies]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movie_descriptions)
    tfidf_vector = tfidf_vectorizer.transform([movie.overview])
    cosine_similarities = cosine_similarity(tfidf_vector, tfidf_matrix).flatten()
    
    similar_movie_indizes = cosine_similarities.argsort()[:-6:-1] #first 5 movies
    similar_movies = [Movie.objects.get(pk=movie_ids[movie_id]) for movie_id in similar_movie_indizes]

    return similar_movies