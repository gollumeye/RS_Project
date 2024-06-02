from movieRecommenderApp.models import Movie, Rating
from movieRecommenderApp.recommendationAlgorithms.popularMoviesOfSameYear import recommend_popular_movies_of_same_year

"""
If the selected movie has user ratings, movies are recommended based on other movies those users have rated
If the selected movie has no user ratings, the popularMoviesOfSameYear() algorithm is used as a fallback
"""
def recommend_movies_by_ratings(movie):
    ratings = Rating.objects.filter(movie_id=movie.id)

    if len(ratings) is 0:
        return recommend_popular_movies_of_same_year(movie)

    user_ids = ratings.values_list('user_id', flat=True).distinct() #get all users that have rated the movie
    other_movies_rated = Rating.objects.filter(user_id__in=user_ids).exclude(movie_id=movie.id) #get other movies that the users have rated

    #get avg rating and number of ratings for each movie that the users have also rated
    movie_ratings = {}
    for rating in other_movies_rated:
        if rating.movie_id not in movie_ratings:
            movie_ratings[rating.movie_id] = {'sum_of_ratings': 0, 'number_of_ratings': 0}
        movie_ratings[rating.movie_id]['sum_of_ratings'] += rating.rating
        movie_ratings[rating.movie_id]['number_of_ratings'] += 1

    for movie_id, rating_data in movie_ratings.items():
        movie_ratings[movie_id]['average_rating'] = rating_data['sum_of_ratings'] / rating_data['number_of_ratings']

    #movies recommended based on the average rating and how often it was rated by the users
    sorted_movies = sorted(movie_ratings.items(), key=lambda x: (x[1]['average_rating'], x[1]['number_of_ratings']), reverse=True)

    similar_movies = []
    counter = 0

    for movie_id, _ in sorted_movies:
        if counter >= 5:
            break
        recommended_movie = Movie.objects.get(pk=movie_id)
        if (movie.adult is False and recommended_movie.adult is True) is False:
            similar_movies.append(recommended_movie)
            counter += 1

    return similar_movies