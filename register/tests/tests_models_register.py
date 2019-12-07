from django.test import TestCase
from register.models import Profile
from django.contrib.auth.models import User


class test_user(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('wafistos4', 'wafi@gmail.com', 'djamel2013')
        self.profile = Profile.objects.get_or_create(user=self.user)
    
    def test_return_model_username(self):
        self.assertEquals(self.profile[0].__str__(), self.user.username)
    