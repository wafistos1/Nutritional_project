from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
from register.models import Profile
from register.forms import UserRegisterForm, profileForm


class TestViewsRegister(TestCase):
    def setUp(self):
        self.client = Client()
        self.Register_url = reverse('register')
        self.compte_url = reverse('compte')
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.profile = Profile.objects.get_or_create(user=self.user, image='picture/wafi.png')
        

    def test_Register_get(self):
        response = self.client.get(self.Register_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/user.html')
        

    def test_compte_get(self):
        self.client.login(username= 'wafi', password='wafipass') 
        response = self.client.get(self.compte_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/compte.html')
        
         
    def test_request_post_is_ok(self):
        count_old = Profile.objects.count()
        response = self.client.post( '/register/register/',
                                     {'username': self.user.username,
                                      'email': self.user.email,
                                      'password1': self.user.password,
                                      'password2': self.user.password,
                                      'image': self.profile[0].image,
                                                 })
        user_profile = User.objects.create_user('wafios', 'wafi1@gmail.com', 'wafipass1')
        profile = Profile.objects.create(
            user=user_profile,
            image=self.profile[0].image
        )
        count_new = Profile.objects.count()
        self.assertEquals(count_old+1, count_new)


    def test_valid_data(self):
        """Testing valid data 
        """
        response = self.client.post( '/register/register/',
                                     {
                                         'username': 'wafistos200',
                                         'email': 'wafi@gmail.com',
                                         'password1': 'toto2013',
                                         'password2': 'toto2013',
                                         'image': '/media/default.jpg',
                                                 })
        form = UserRegisterForm({
            'username': 'wafistos201',
            'email': 'wafi@gmail.com',
            'password1': 'toto2013',
            'password2': 'toto2013',
        })
        form_profile = profileForm(data={
            'user': form,
            'image': '/media/default.jpg',
            
            })

        self.assertTrue(form.is_valid() and form_profile.is_valid())
        if form.is_valid() and form_profile.is_valid():
            user = form.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
        self.assertEqual(profile.user.username, "wafistos201")
        self.assertEqual(profile.user.email, "wafi@gmail.com")
        self.assertEqual(profile.image.url, "/media/default.jpg")
