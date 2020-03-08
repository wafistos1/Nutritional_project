from rest_framework import serializers
from .models import Product

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'grade',  
            'images', 
            'categorie', 
            'detail_igredient', 
            'url',
            'detail_nutrition_url',
            ]