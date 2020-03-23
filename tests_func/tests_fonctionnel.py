from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.urls import reverse
from store.models import Product, Favorite, Categorie
from register.models import Profile
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
import time 
import requests
from selenium import webdriver

class MySeleniumTests(LiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver(executable_path='C:/geckodriver.exe')
        self.selenium.implicitly_wait(10)        
        self.user = User.objects.create_user('wafistos4', 'wafi@gmail.com', 'djamel2013')
        self.categorie = Categorie.objects.create(name='Soda')
        self.profile = Profile.objects.get_or_create(user=self.user, image='picture/wafi.png')
        self.product_favorite = Product.objects.create(
            name='cafe',
            grade='A', 
            images='static/img/23.jpg', 
            categorie=self.categorie
            )        
        self.product_choice = Product.objects.create(
            name='Cafe', 
            grade='B', 
            images='static/img/123.jpg', 
            categorie=self.categorie
            )

        self.favorite = Favorite.objects.create(
                    product_choice=self.product_choice,
                    product_favorite=self.product_favorite,
                    user=self.user
                    )
    
    def tearDown(self):
        self.selenium.quit()

       
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/login/'))
        self.selenium.find_element_by_id("id_username").send_keys('wafistos4')
        self.selenium.find_element_by_id("id_password").send_keys('djamel2013')
        self.selenium.find_element_by_id('submitBtn').click()
        self.assertEquals(self.selenium.title, 'Home')


    def test_search(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/store'))
        query = self.selenium.find_element_by_name("q")
        query.send_keys('Pepsi')
        self.selenium.find_element_by_id('submitId').click()
        

    def test_rating(self):
        url_rating = f"/detail_favori/{self.favorite.id}"
        self.selenium.get('%s%s' % (self.live_server_url, url_rating))
        self.selenium.find_element_by_id("id_username").send_keys('wafistos4')
        self.selenium.find_element_by_id("id_password").send_keys('djamel2013')
        self.selenium.find_element_by_id('submitBtn').click()
        self.selenium.find_element_by_xpath('//div[@class="rating"]/a[@id="rate_id"]').click()
        
        

        
        
        
        
        