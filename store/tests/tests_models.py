from django.test import TestCase
from store.models import Product, Favorite, Categorie
from register.models import Profile
from django.contrib.auth.models import User




class TestModels(TestCase):

    def setUp(self):
        self.categorie = Categorie.objects.create(name='soda')
        self.product_choice = Product.objects.create(name='coca', grade='C', images='static/img/123.jpg', categorie=self.categorie)
        self.product_favorite = Product.objects.create(name='pepsi', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.favorite = Favorite.objects.create(product_choice=self.product_choice, product_favorite=self.product_favorite, user=self.user)

    def test_favorite_objects_product_choice_name(self):
        self.assertEquals(self.favorite.product_choice.name, 'coca')

    def test_favorite_objects_product_favorite_name(self):
        self.assertEquals(self.favorite.product_favorite.name, 'pepsi')

    def test_favorite_objects_user_username(self):
        self.assertEquals(self.favorite.user.username, 'wafi')

    def test_favorite_objects_product_categorie(self):
        self.assertEquals(self.favorite.product_choice.categorie.name, 'soda')

    def test_favorite_objects_product_favorite_image_path(self):
        self.assertEquals(self.favorite.product_favorite.images, 'static/img/23.jpg')
    
    def test_favorite_objects_product_choice_image_path(self):
        self.assertEquals(self.favorite.product_choice.images, 'static/img/123.jpg')
    
    def test_favorite_objects_product_favorite_grade(self):
        self.assertEquals(self.favorite.product_favorite.grade, 'A')
    
    def test_favorite_objects_product_choice_grade(self):
        self.assertEquals(self.favorite.product_choice.grade, 'C')