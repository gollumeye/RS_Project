Step 0: Download the following datasets and put them in the project repository:

MovieLens 20M Dataset from https://grouplens.org/datasets/movielens/

Posters from https://www.kaggle.com/datasets/ghrzarea/movielens-20m-posters-for-machine-learning
-> here put (only) the folder "MLP-20M" containing the images into the folder "static" of the project

Additional Movie Information from https://drive.google.com/file/d/1je77e0Lq8naVUsjoOzk5RuI2H3ceHlSz/view
________________________________________________________________________________________________________________________

Step 1: Activate virtual environment and install django and psycopg2 and other needed dependencies

Step 2: Create database "rs_project" and update username and pw in the settings.py file.
In the database run "CREATE EXTENSION pg_trgm;"

Step 3: run "python manage.py makemigrations" and then "python manage.py migrate"

Step 4: run "db_script.py" to populate the database (update username and pw of database first)

Step 5: run "python manage.py runserver" to start the server and application (runs on localhost)