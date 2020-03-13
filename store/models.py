from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Categorie(models.Model):
    """
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """ Class
    """
    GRADE_CHOICE = [
        ('a','a'),
        ('b','b'),
        ('c','c'),
        ('d','d'),
        ('e','e'),
        ('unknown','unknown'),   
    ]
    name = models.CharField(_('Nom produit'), max_length=500, unique=True)
    grade = models.CharField(max_length=40, choices=GRADE_CHOICE)
    images = models.URLField(max_length=500)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    detail_igredient = models.TextField(default='None')
    url = models.URLField(max_length=500, default='None')
    detail_nutrition_url = models.URLField(max_length=500, default='None')
    
    

    def __str__(self):
        return self.name

class Favorite(models.Model):
    """ Class of favorite user
    """

    product_choice = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='PK_product_choice'
        )
    product_favorite = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='PK_product_favorite'
        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"produit: {self.product_choice.name} , product_substitute:{self.product_favorite.name}"


class Rating(models.Model):
    """Models of the products rating system 
    """
    RATE_CHOICE = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
        ('0','0'),   
    ]
    rating = models.PositiveIntegerField(null=True, choices=RATE_CHOICE)
    product_rating = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_rating = models.ForeignKey(User, on_delete=models.CASCADE)
    user_voting = models.BooleanField(default=False)
    class Meta:
        db_table = 'Rating'
        constraints = [
            models.UniqueConstraint(fields=['user_rating', 'product_rating'], name='reservation_unique')
        ]