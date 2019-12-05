from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from register.models import Profile
from django.test.client import RequestFactory

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

    def test_request_post(self):
        old_users_num = User.objects.count()
        profile_name = self.user.username
        profile_email = self.user.email
        profile_password1 = self.user.password
        profile_password2 = self.user.password
        
        response = self.client.post(reverse('register'),
                                     {'username': profile_name,
                                      'email': profile_email,
                                      'password1': profile_password1,
                                      'password2': profile_password2,
                                                 })
        
        
        
        new_users_num = User.objects.count()
        self.assertEquals(old_users_num + 1, new_users_num)
         