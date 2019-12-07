from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from store.models import Product, Favorite, Categorie
from register.models import Profile
from django.core.paginator import Paginator, EmptyPage

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.resultats_url = reverse('resultats' )
        self.aliment_url = reverse('aliment')
        self.home_url = reverse('home')
        self.save_aliment_url = reverse('save_aliment', args=[1, 2])
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.categorie = Categorie.objects.create(name='Soda')
        self.product_favorite = Product.objects.create(name='Pepsi', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        self.product_choice = Product.objects.create(name='Cafe', grade='B', images='static/img/123.jpg', categorie=self.categorie)
        self.paginator = Paginator(self.product_favorite, 15)
        self.favorite = Favorite.objects.create(
            product_choice=self.product_choice,
            product_favorite=self.product_favorite,
            user=self.user
            )
    
    def test_home_get(self):
            response = self.client.get(self.home_url)
            self.assertEquals(response.status_code, 200)

    def test_resultats_get(self):# 
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get('/store/resultats?&q=Pepsi')
        search_product = Product.objects.filter(name='Pepsi').first()
        self.assertEquals(search_product.name, 'Pepsi')
        self.assertEquals(search_product.grade, 'A')
        self.assertEquals(search_product.categorie, self.categorie)
        self.assertEquals(response.status_code, 200)
        
    def test_resultats_get_best_product(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get('/store/resultats?&q=Cafe')
        search_product = Product.objects.filter(name='Cafe').first()
        best_product = Product.objects.filter(categorie=search_product.categorie).filter(grade__lt=search_product.grade).order_by('grade').first()
        self.assertEquals(best_product.name, 'Pepsi')
        self.assertEquals(best_product.grade, 'A')
        self.assertEquals(best_product.categorie, self.categorie)
        self.assertEquals(response.status_code, 200)
    
    def test_resultats_get_no_product_find(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get('/store/resultats?&q=balablato')
        search_product = Product.objects.filter(name='balablato')
        number_of_search_product = search_product.count()
        self.assertEquals(number_of_search_product, 0)
        self.assertEquals(response.status_code, 200)

        
    def test_aliment_get(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(self.aliment_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/aliment.html')

    def test_resultats_get_redirect(self):
        response = self.client.get(self.resultats_url)
        self.assertEquals(response.status_code, 302)

    def test_aliment_get_redirect(self):
        response = self.client.get(self.aliment_url)
        self.assertEquals(response.status_code, 302)
    
    
    def test_save_aliment_redirect(self):
        response = self.client.get(self.save_aliment_url)
        self.assertEquals(response.status_code, 302)
    
    def test_pagination_returns_last_page_if_page_out_of_range(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get('/store/resultats/1')
               
        # Check that if page is out of range (e.g. 999), deliver last page of results
       
        
               
    def test_save_aliment_is_ok(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(f'/store/aliment/{self.product_choice.id}/{self.product_favorite.id}/')
        product_choice = Product.objects.filter(pk=self.product_choice.id)
        product_favorite = Product.objects.filter(pk=self.product_favorite.id)
        favorite = Favorite.objects.get_or_create(
            product_choice=product_choice[0],
            product_favorite=product_favorite[0],
            user=self.user
        )
        self.assertEquals(favorite[0].product_choice.name , 'Cafe')
        self.assertEquals(response.status_code, 200)
        
        
    
    def test_delete_aliment_is_ok(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(f'/store/aliment_delete/{self.favorite.id}')
        delete_favorite = Favorite.objects.filter(id=self.favorite.id, user=self.user)
        if delete_favorite.exists():
            
            delete_favorite.delete()
        self.assertQuerysetEqual(delete_favorite, [])
        
    
    def test_delete_aliment_is_not_ok(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(f'/store/aliment_delete/1000000000')
        delete_favorite = Favorite.objects.filter(id=None)
        self.assertEquals(response.status_code, 200)
        

         
         
    """
    # todo Reste a teste
    def resultats(request, page=1): 
     1-query = request.GET.get('q').capitalize()
     2-best_product = Product.objects.filter(categorie=data[0].categorie).filter(grade__lt=data[0].grade).order_by("grade")
     3-send_text = "essayez une autre recherche!!"
     4-except EmptyPage:
     
    def save_aliment(request, fav, prod): 
     1-favorite_product = Product.objects.filter(pk=fav)
     2-favorite = Favorite.objects.get_or_create( ...)
     3-return render(request, 'store/save_aliment.html', {'favorite': favorite[0]})
     
    def detail_favori(request, pk): 
    1-favorite = Favorite.objects.filter(pk=pk, user=request.user) 
    2-return render(request, 'store/detail_favori.html', {'favorite': favorite[0]})
    
    def aliment_delete(request, pk):
    1-favorite = Favorite.objects.filter(pk=pk, user=request.user)
    2-if favorite.exists():
    3-else: 
    4-return render(request, 'store/aliment_delete.html')
    """