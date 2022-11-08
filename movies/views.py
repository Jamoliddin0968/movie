from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import permissions 
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView 
from .models import Movie, Actor
from rest_framework.views import APIView
from .functions import get_client_ip, MovieFilter
from .serializers import (
    MovieListSerializers,
    MovieDetailSerializer,
    ReviewCreateSerializers,
    ActorListSerializers,
    RatingCreateSerializers,
    UserSerializer
)


class MovieListView(ListAPIView):

    # filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(
                                         ratings__ip=get_client_ip(self.request))
                                     )
        ).annotate(
            midlle_star=models.Sum(models.F("ratings__star")) /
            models.Count(models.F("ratings"))
        )
        return movies
    serializer_class = MovieListSerializers
# kinolar ro'yhati


class MovieDetailView(RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
# bitta kino


class ReviewCreateView(CreateAPIView):
    serializer_class = ReviewCreateSerializers


class ActorListView(ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializers


class AddRating(CreateAPIView):
    serializer_class = RatingCreateSerializers

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class UserView(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({"User": user.data})
