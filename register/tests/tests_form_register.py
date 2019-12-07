from register.models import Profile
from django.test import TestCase
from django.contrib.auth.models import User
from register.forms import UserRegisterForm

class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('wafi', 'wafi@gmail.com', 'wafipass')
        self.profile = Profile.objects.get_or_create(user=self.user, image='picture/wafi.png')
        
    

    def test_renew_form_date_too_far_in_future(self):
        form_data = {'username': self.user.username,
                     'email': self.user.email,
                     'password1': self.user.password,
                     'password2': self.user.password,
                     'image': self.profile[0].image,
                     }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

