from django.urls import path
from .views import MovieListView , MovieDetailView , ReviewCreateView , ActorListView , AddRating

urlpatterns = [
    path("movie/",MovieListView.as_view()),
    path("movie/<int:pk>/",MovieDetailView.as_view()),
    path("review/",ReviewCreateView.as_view()),
    path("actor/",ActorListView.as_view()),
    path("star/",AddRating.as_view()),
]