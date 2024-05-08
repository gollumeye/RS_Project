from django.urls import path

from . import views
from .views import movie_search

urlpatterns = [
    path('', movie_search, name='movie_search'),
    path('recommendations/<int:movie_id>/', views.recommendations, name='recommendations'),
]