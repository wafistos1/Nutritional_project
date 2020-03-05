"""Module views the application store for displaying templates
"""
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages import SUCCESS, ERROR
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from store.models import Product, Favorite, Rating
from django.views.decorators.csrf import csrf_exempt

# Global variable
query = None


def home(request):
    """Displays the main page.
    """
    return render(request, 'store/home.html')


@login_required(login_url='login')
def resultats(request, page=1):
    """Displays the results of the search for substitute products
    """

    global query
    if request.GET.get('q') is not None:
        query = request.GET.get('q').capitalize()
    try:
        data = Product.objects.filter(name__contains=query)
        best_product = Product.objects.filter(
            categorie=data[0].categorie
            ).filter(grade__lt=data[0].grade).order_by("grade")
        if not best_product:
            text = _('Vous avez choisi le meilleur produit nutitionnelle')
            return render(
                request, 'store/resultats.html',
                {'data': data[0], 'best_product': best_product, 'text': text}
                )
        paginator = Paginator(best_product, 15)
        best_product = paginator.page(page)
    except IndexError:
        send_text = _("Essayez un autre produit.")
        produit = query
        return render(request, 'store/home.html', {'text': send_text, 'produit': produit})
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)
    return render(request, 'store/resultats.html', {'data': data[0], 'best_product': best_product})


@login_required(login_url='login')
def aliment(request):
    """Display all aliment favorite of user
    """
    favorite = Favorite.objects.filter(
        user=request.user).select_related('product_choice', 'product_favorite', 'user')
        
    return render(request, 'store/aliment.html', {'favorites': favorite, 'rating': rating})


@login_required(login_url='login')
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


@login_required(login_url='login')
def detail_favori(request, pk):
    """
    Views who display details of the favorite product
    """
    favorite = Favorite.objects.filter(pk=pk, user=request.user)
    return render(request, 'store/detail_favori.html', {'favorite': favorite[0]})


@login_required(login_url='login')
def aliment_delete(request, pk):
    """
    Views to delete product of favorite list
    """
    favorite = Favorite.objects.filter(pk=pk, user=request.user)
    if favorite.exists():
        if request.user == favorite[0].user:
            favorite[0].delete()
            messages.add_message(request, SUCCESS, _('Produit supprimer avec succès '))
        else:
            messages.add_message(
                request, ERROR,
                _("On ne peut pas supprimer ces produits car vous n'êtes pas le propriétaire  ")
                )
    return render(request, 'store/aliment_delete.html')

def mention(request):
    """Mentions legales
    """
    return render(request, 'store/mentions.html')

@csrf_exempt
def rating(request):
    """Displays the results of the search for substitute products
    """
    # 1 faire une recherche si l'utilisateur a deja voter.
    # 2 si la reponse est non on cree un objet du model Rating avec la note et id du l'utilisateur.
    # 3 prend la moyen des notes et le nombre des votant( utilisateurs)" requete sql calculer la moyen" pour l'affiche.
    # 4 envoye la moyenne des notes et le nombres des utilisateurs en format Json.
    
    if request.method == 'POST':
        
        query = request.POST
        rating = int(query['rate'])   
        product_id = query['id']
        product = Product.objects.get(pk=product_id)
        user_rating = request.user
        rating_model = Rating.objects.get_or_create(
            rating=rating,
            product_rating=product,
            user_rating=user_rating,
            user_voting=True
            )
        # Change types into string and int for sending in HttpResponse.
        rating = int(rating_model[0].rating)
        product_rating = str(rating_model[0].product_rating)
        user_rating = str(rating_model[0].user_rating)
        user_voting =  str(rating_model[0].user_voting)
        context = {
            'rating': rating,
            'product_rating': product_rating,
            'user_rating': user_rating,
            'user_voting': user_voting,
            }
        
        dump = json.dumps(context)
        return HttpResponse(dump, content_type='application/json')

        # try:
        #     rating_model = Rating.objects.get_or_create(
        #     rating=rating,
        #     product_rating=product,
        #     user_rating=user_rating,
        #     user_voting=True
        #     )
        #     context = {
        #     'data': rating_model[0]
        #     }
        
        #     dump = json.dumps(context)
        #     return HttpResponse(dump, content_type='application/json')
        # except:
        #     print('toto')
            

            # context = {
            #     'data': " Une erreure c'est produite"
            # }
            # dump = json.dumps(context)
            # print(type(context))
            # print(type(dump))
            # return HttpResponse(dump, content_type='application/json')