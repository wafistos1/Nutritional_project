from django.test import TestCase
from register.models import Profile
from django.contrib.auth.models import User


class test_user(TestCase):
    pass
    # def setUp(self):
    #     self.user = User.objects.create_user('wafistos4', 'wafi@gmail.com', 'djamel2013')
    #     self.profile = Profile.objects.get_or_create(user=self.user)
        
    # def test_deactivate(self):
    #     self.user.deactivate()
    #     self.assertFalse(self.user.avtive)
        
    # def test_deactivate_activate(self):
    #     self.user.deactivate()
    #     self.user.activate()
    #     self.assertTrue(self.user.active)
    