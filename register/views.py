from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from register.forms import profileForm, UserRegisterForm



def Register(request):
    """ function for user registration
    """
    if request.method == "POST":      
        user_form = UserRegisterForm(request.POST)
        profile_form = profileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('compte')
    else:
        user_form = UserRegisterForm()
        profile_form = profileForm()
    return render(request, 'register/user.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required(login_url = 'login')
def compte(request):
    """ Display Details of User
    """
    return render(request, 'register/compte.html', locals())