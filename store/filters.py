import django_filters
from .models import Product, Rating

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['grade', 'categorie']


class RatingFilter(django_filters.FilterSet):
    class Meta:
        model = Rating
        fields = ['rating',]