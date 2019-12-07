from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from register.models import Profile
from django.test.client import RequestFactory
import json
class TestViewsRegister(TestCase):
    def setUp(self):
        self.client = Client()
        self.Register_url = reverse('register')
        self.compte_url = reverse('compte')
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.profile = Profile.objects.get_or_create(user=self.user)
        


    def test_Register_get(self):
        response = self.client.get(self.Register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/user.html')

    def test_compte_get(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(self.compte_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/compte.html')

    def test_request_post_is_ok(self):# todo voir avec le mentor pour explication
        
        response = self.client.post('/register/register')
        self.assertEquals(response.status_code, 302)
         
    def test_request_post_is_not_ok(self):# todo voir avec le mentor pour explication
        
        response = self.client.post( '/admin',
                                     {'username': self.user.username,
                                      'password': self.user.password,
                                                 })
        print(response)
        self.assertEquals(response.status_code, 302)
    
    