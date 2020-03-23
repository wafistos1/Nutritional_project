from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse, resolve
from store.models import Product, Favorite, Categorie, Rating
from register.models import Profile
from django.core.paginator import Paginator, EmptyPage
from store.filters import  ProductFilter, RatingFilter


class TestViews(TestCase):
    def setUp(self):
<<<<<<< HEAD
        request = self.factory.get('/customer/details')
=======
        self.factory = RequestFactory
>>>>>>> staging
        self.client = Client()
        url = reverse('home')
        self.response = self.client.post(url)
        self.resultats_url = reverse('resultats' )
        self.filter_url = reverse('filter' )
        self.aliment_url = reverse('aliment')
        self.home_url = reverse('home')
        self.save_aliment_url = reverse('save_aliment', args=[1, 2])
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.categorie = Categorie.objects.create(name='Soda')
        self.product_favorite = Product.objects.create(name='Pepsi', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        self.product_favorite1 = Product.objects.create(name='cafe', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        self.product_choice = Product.objects.create(name='Cafe', grade='B', images='static/img/123.jpg', categorie=self.categorie)
        self.paginator = Paginator(self.product_favorite, 15)
        self.all_product = Product.objects.all()
        self.all_product_rating = Rating.objects.all()
        self.favorite = Favorite.objects.create(
            product_choice=self.product_choice,
            product_favorite=self.product_favorite,
            user=self.user
            )
<<<<<<< HEAD
        self.product_filter = ProductFilter(request.GET, queryset=self.all_product())
        self.rating_filter = RatingFilter(request.GET, queryset=self.all_product_rating)
=======
        self.rating = Rating.objects.create(
            rating='3',
            product_rating=self.product_choice,
            user_rating=self.user,
            user_voting=True,
            )
>>>>>>> staging
    
    def test_home_get(self):
            response = self.client.get('/store/')
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed( 'home.html')

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
        self.assertEquals(best_product.name, 'cafe')
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
        
    def test_detail_fovorite(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(f'/store/detail_favori/{self.favorite.id}')
        favorite = Favorite.objects.filter(id=self.favorite.id)
        self.assertEquals(response.status_code, 200)
        
<<<<<<< HEAD
    def test_product_filter_is_ok(self):
        self.product_filter
=======
    def test_rating_create_models(self):
        self.client.login(username= 'wafi', password='wafipass')
        response = self.client.get(f'/store/detail_favori/{self.favorite.id}')
        rating_favorite = Rating.objects.create(
            rating='3',
            product_rating=self.favorite.product_favorite,
            user_rating=self.user,
            user_voting=True,
        )
        self.assertEquals(rating_favorite.product_rating, self.favorite.product_favorite)
        self.assertEquals(rating_favorite.user_rating, self.user)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(rating_favorite.rating, self.rating.rating )

    def test_if_filter_is_ok(self):
        self.client.login(username= 'wafi', password='wafipass')
        response = self.client.get('/resultats?&q=Mozzarella')
        search_product = Product.objects.create(name='Mozzarella', grade='A', images='static/img/23.jpg', categorie=self.categorie)
        response1 = self.client.get('/filter?grade=b&categorie=1&rating=3')
        try:
            rating = Rating.objects.create(
                rating='4',
                product_rating=self.product_favorite1,
                user_rating=self.user,
                user_voting=True,
                )
        except:
            pass
        self.assertEquals(rating.rating, '4')
        self.assertEquals(rating.product_rating, self.product_favorite1)
        self.assertEquals(rating.user_rating, self.user)
        self.assertEquals(rating.user_voting, True)
        self.assertEquals(response1.status_code, 200)

    
    def test_rating_send_post_is_ok_context(self):
        self.client.login(username= 'wafi', password='wafipass')
        response = self.client.get(f'/detail_favori/{self.favorite.id}')
 
        
        self.assertEquals(response.status_code, 200)


>>>>>>> staging
         
         
    """

    """