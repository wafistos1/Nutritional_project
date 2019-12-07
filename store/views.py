from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, Favorite, Categorie
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Global variable
query = None

def home(request):
    return render(request, 'store/home.html')


@login_required(login_url = 'login')
def resultats(request, page=1):
    """Displays the results of the search for substitute products 
    """
    global query 
    if request.GET.get('q') is not None :
        query = request.GET.get('q').capitalize()
    try:
        data = Product.objects.filter(name__contains=query)
        best_product = Product.objects.filter(categorie=data[0].categorie).filter(grade__lt=data[0].grade).order_by("grade")
        paginator = Paginator(best_product, 15)
        best_product = paginator.page(page)
    except IndexError:
        send_text = "Essayez un autre produit."
        produit = query 
        return render(request, 'store/home.html', {'text': send_text, 'produit': produit})
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)
    return render(request, 'store/resultats.html', {'data': data[0], 'best_product': best_product})


@login_required(login_url = 'login')
def aliment(request):
    """Display all aliment favorite of user
    """
    favorite = Favorite.objects.filter(user=request.user).select_related('product_choice', 'product_favorite', 'user')
    return render(request, 'store/aliment.html', {'favorites': favorite})


@login_required(login_url = 'login')
def save_aliment(request, fav, prod):
    """saves the food that the user has chosen in the database
    """
    favorite_product = Product.objects.filter(pk=fav)
    choice_product = Product.objects.filter(pk=prod)
    favorite = Favorite.objects.get_or_create(
        product_choice=choice_product[0],
        product_favorite=favorite_product[0],
        user=request.user
        )
    return render(request, 'store/save_aliment.html', {'favorite': favorite[0]})


@login_required(login_url = 'login')
def detail_favori(request, pk):
    favorite = Favorite.objects.filter(pk=pk, user=request.user)
    return render(request, 'store/detail_favori.html', {'favorite': favorite[0]})


@login_required(login_url = 'login')
def aliment_delete(request, pk):

    favorite = Favorite.objects.filter(pk=pk, user=request.user)
    if favorite.exists():
        if request.user == favorite[0].user:
            favorite[0].delete()
        else:
            print('pas le meme user')
    return render(request, 'store/aliment_delete.html')
