from django.contrib.auth.models import User
from django import forms
from register.models import Profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    """ Class form for user registration
    """
    email = forms.EmailField()


    def __init__(self, *args, **kwargs):
        """Hide help message for register user
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        """ Display field to input text
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name']


class profileForm(ModelForm):
    class Meta:
        model = Profile
        fiels = ('image', )
        exclude = ['user']
        