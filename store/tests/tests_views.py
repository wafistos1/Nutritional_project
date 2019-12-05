from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from store.models import Product, Favorite, Categorie
from register.models import Profile
from django.core.paginator import Paginator, EmptyPage
from django.test.client import RequestFactory


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.resultats_url = reverse('resultats')
        self.aliment_url = reverse('aliment')
        self.home_url = reverse('home')
        self.save_aliment_url = reverse('save_aliment', args=[1, 2])
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.categorie = Categorie.objects.create(name='Soda')
        self.product_favorite = Product.objects.create(name='pepsi', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        self.paginator = Paginator(self.product_favorite, 15)
        self.factory = RequestFactory()


    def test_home_get(self):
            response = self.client.get(self.home_url)
            self.assertEquals(response.status_code, 200)

    def test_resultats_get(self):
        self.client.login(username= 'wafi', password='wafipass') 
        request = self.factory.get('/store/resultats/')
        response = self.client.get(request)
        print(response.context)
        
        self.assertEquals(response.status_code, 404)

    def test_aliment_get(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(self.aliment_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/aliment.html')
    
    
    def save_aliment(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(self.save_aliment_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/save_aliment.html')


    def test_resultats_get_redirect(self):
        response = self.client.get(self.resultats_url)
        self.assertEquals(response.status_code, 302)

    def test_aliment_get_redirect(self):
        response = self.client.get(self.aliment_url)
        self.assertEquals(response.status_code, 302)
    
    
    def save_aliment_redirect(self):
        response = self.client.get(self.save_aliment_url)
        self.assertEquals(response.status_code, 302)
    
    def test_pagination_returns_last_page_if_page_out_of_range(self):
        self.client.login(username= 'wafi', password='wafipass') 
        request = self.factory.get('/store/resultats/')
        response = self.client.get(request)        
        # Check that if page is out of range (e.g. 999), deliver last page of results