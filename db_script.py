import csv
import json
import os

import psycopg2
from psycopg2 import extras

dbname = "postgres"
user = "postgres"
password = "postgres" #PUT PASSWORD HERE
host = "localhost"
port = "5432"

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

ratings_file = "ml-20m/ratings.csv"
tags_file = "ml-20m/genome-tags.csv"
genome_scores_file = "ml-20m/genome-scores.csv"
movie_details_path = "extracted_content_ml-latest"

# ---------------------------------------------------------------
# RATINGS

print("reading ratings...")
data = []
with open(ratings_file, "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        user_id = int(row[0])
        movie_id = int(row[1])
        rating = float(row[2])
        data.append((user_id, movie_id, rating))

ratings_query = """
    INSERT INTO "movieRecommenderApp_rating" ("user_id", "movie_id", "rating")
    VALUES %s
"""

print("inserting ratings...")
extras.execute_values(cur, ratings_query, data)

print("inserted ratings successfully")

# ----------------------------------------------------------
# TAGS

print("reading tags...")

data = []
with open(tags_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        tag_id = int(row[0])
        tag_name = row[1]
        data.append((tag_id, tag_name))

print("inserting tags...")

tags_query = """
    INSERT INTO "movieRecommenderApp_tag" ("tag_id", "tag_name")
    VALUES %s
"""

extras.execute_values(cur, tags_query, data)

print("tags inserted successfully")

# ----------------------------------------------------------
# MOVIES

print("reading & inserting movie details...")

for filename in os.listdir(movie_details_path):
    if filename.endswith(".json"):
        file_path = os.path.join(movie_details_path, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            movie_data = json.load(file)

        movielens_data = movie_data.get("movielens", {})
        movielens_id = movie_data.get("movielensId")
        title = movielens_data.get("title")
        genres = movielens_data.get("genres", [])
        release_year = movielens_data.get("releaseYear")
        actors = movielens_data.get("actors", [])

        tmdb_data = movie_data.get("tmdb", {})
        popularity = tmdb_data.get("popularity")
        overview = tmdb_data.get("overview")
        vote_average = tmdb_data.get("vote_average")
        adult = tmdb_data.get("adult")

        imdb_data = movie_data.get("imdb", {})
        writers = imdb_data.get("writers", [])
        production_companies = imdb_data.get("productionCompanies", [])
        directors = imdb_data.get("directors", [])

        movie_query = """
            INSERT INTO "movieRecommenderApp_movie" ("id", "genres", "title", "release_year", "actors", "popularity", "overview", "vote_average", "adult", "writers", "production_companies", "directors")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(movie_query, (
        movielens_id, genres, title, release_year, actors, popularity, overview, vote_average, adult if adult is not None else False, writers,
        production_companies, directors))

print("inserted movie data successfully")

# ----------------------------------------------------------
# TAGS PER MOVIE

print("reading movie tags...")

tags_dict = {}
with open(genome_scores_file, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        movie_id = int(row[0])
        tag_id = int(row[1])
        relevance = float(row[2])
        if relevance > 0.5: #only consider tags that have a high relevance score
            if movie_id not in tags_dict:
                tags_dict[movie_id] = []
            tags_dict[movie_id].append(tag_id)

print("inserting movie tags...")

for movie_id, relevant_tags in tags_dict.items():
    update_query = """
        UPDATE "movieRecommenderApp_movie"
        SET "tags_ids" = %s
        WHERE "id" = %s
    """
    cur.execute(update_query, (relevant_tags, movie_id))

print("inserted movie tags successfully")

conn.commit()
cur.close()
conn.close()

print("Inserted all data successfully!")
