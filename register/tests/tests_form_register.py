# import datetime
from django.test import TestCase

from register.forms import UserRegisterForm

class UserRegisterFormTest(TestCase):
    pass

    # def test_renew_form_date_too_far_in_future(self):
    #     date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
    #     form = UserRegisterForm(data={'renewal_date': date})
    #     self.assertFalse(form.is_valid())

    # def test_renew_form_date_today(self):
    #     date = datetime.date.today()
    #     form = UserRegisterForm(data={'renewal_date': date})
    #     self.assertTrue(form.is_valid())
        
    # def test_renew_form_date_max(self):
    #     date = timezone.localtime() + datetime.timedelta(weeks=4)
    #     form = UserRegisterForm(data={'renewal_date': date})
    #     self.assertTrue(form.is_valid())