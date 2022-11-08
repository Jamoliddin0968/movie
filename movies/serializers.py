from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from django.forms import models
from django.template import context
from rest_framework import serializers
from django.db import models

from .models import Movie , Review , Rating , Actor

class FilterReviewSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent = None)
        return super().to_representation(data)

class ReviewRekursivSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__( value ,context = self.context)
        return serializer.data

class ActorListSerializers(serializers.ModelSerializer):
    """actyorlar"""
    class Meta:
        model = Actor
        fields = "__all__"

class MovieListSerializers(serializers.ModelSerializer):
    """kinoga"""
    rating_user = serializers.BooleanField()
    midlle_star = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ("title","tagline","rating_user","midlle_star")

class ReviewCreateSerializers(serializers.ModelSerializer):
    "otziv"
    class Meta:
        model = Review
        fields = "__all__"

class ReviewSerializers(serializers.ModelSerializer):
    """otziv"""
    children = ReviewRekursivSerializer(many=True)
    class Meta:
        list_serializer_class = FilterReviewSerializer
        model = Review
        fields = ("email","text","children")

class MovieDetailSerializer(serializers.ModelSerializer):
    """bittaliga"""
    actors = ActorListSerializers(read_only = True,many = True)
    reviews = ReviewSerializers(many = True)
    class Meta:
        model = Movie
        exclude = ("draft",)

class RatingCreateSerializers(serializers.ModelSerializer):
    """reyting qo'shish"""
    class Meta:
        model = Rating
        fields = ("star","movie")

    def create(self, validated_data):
        rating , _ = Rating.objects.update_or_create(
            ip = validated_data.get("ip",None),
            movie = validated_data.get("movie",None),
            defaults={'star':validated_data.get("star")}
        )
        return rating

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ("username", 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user