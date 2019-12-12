from register.models import Profile
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from register.forms import UserRegisterForm, profileForm


class UserRegisterFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('wafistos2000', 'wafi@gmail.com', 'wafipass')
        self.profile = Profile.objects.get_or_create(user=self.user, image='picture/wafi.png')
        self.form_data = {'name': 'wafistos2001',
                'email': 'wafi@gmail.com',
                'password1': 'toto2013',
                'password2': 'toto2013',
                }
        self.form_prfile_data = {
            'image': 'img/picture/wafi.jpg'
        }

    def test_renew_form_date_too_far_in_future(self):
        form = UserRegisterForm(data = {
            'username': 'wafi',
            'email': 'wafi@gmail.com',
            'password1': 'toto2013',
            'password2': 'toto2013',
                })
        form_profile = profileForm(data=self.form_data)
        self.assertTrue(form.is_valid()  )
        self.assertTrue(form_profile.is_valid()  )

    def test_valid_data(self):
        form = UserRegisterForm({
            'username': 'wafistos2034',
            'email': 'wafi@gmail.com',
            'password1': 'toto2013',
            'password2': 'toto2013',
        })
        form_profile = profileForm(data={
            'user': form,
            'image': '/media/default.jpg',
            
            })
        self.assertTrue(form.is_valid() and form_profile.is_valid())
        user = form.save()
        profile = form_profile.save(commit=False)
        profile.user = user
        profile.save()
        self.assertEqual(profile.user.username, "wafistos2034")
        self.assertEqual(profile.user.email, "wafi@gmail.com")
        self.assertEqual(profile.image.url, "/media/default.jpg")