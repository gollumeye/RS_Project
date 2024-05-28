from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from movieRecommenderApp.models import Movie


def recommend_similar_movies_by_description(movie):
    movies_query = Movie.objects.exclude(pk=movie.id) \
        .exclude(overview__isnull=True) \
        .exclude(overview__exact='')

    movies = movies_query
    movie_descriptions = [mov.overview for mov in movies]
    movie_ids = [mov.pk for mov in movies]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(movie_descriptions)
    tfidf_vector = tfidf_vectorizer.transform([movie.overview])
    cosine_similarities = cosine_similarity(tfidf_vector, tfidf_matrix).flatten()
    
    similar_movie_indizes = cosine_similarities.argsort()[:-6:-1] #first 5 movies
    similar_movies = [Movie.objects.get(pk=movie_ids[movie_id]) for movie_id in similar_movie_indizes]

    return similar_movies