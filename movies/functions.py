from codecs import lookup
from dataclasses import field, fields
from pyexpat import model
from django_filters import rest_framework as filters
from movies.models import Movie 
"""ip adres olish uchun funksiya"""

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class CharInFilter(filters.BaseInFilter,filters.CharFilter):
    pass

class MovieFilter(filters.FilterSet):
    year = filters.RangeFilter()
    genres = CharInFilter(field_name = 'genres__name',lookup_expr = 'in')

    class Meta:
        model = Movie
        fields = ('genres','year')
