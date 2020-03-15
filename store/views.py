"""Module views the application store for displaying templates
"""
import json
from django.http import JsonResponse, HttpResponse
from django.urls import NoReverseMatch
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import SUCCESS, ERROR
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from store.models import Product, Favorite, Rating
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Q
from django.core import exceptions, serializers
from .serializers import productSerializer
from .filters import ProductFilter, RatingFilter
from django.views.generic import ListView


# Global variable
query = None
data = None


def home(request):
    """Displays the main page.
    """
    return render(request, 'store/home.html')


@login_required(login_url='login')
def resultats(request, page=1):
    """Displays the results of the search for substitute products
    """

    global query
    # First logic section   
    
    filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
    filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())

    """ Logic of first user search( get best product (best grade )) 
    """
    if request.GET.get('q') is not None:
         query = request.GET.get('q').capitalize()

    try:
        data = Product.objects.filter(name__contains=query)
        best_product = Product.objects.filter(
            categorie=data[0].categorie
            ).filter(grade__lt=data[0].grade).order_by("grade")
        if  best_product is None:
            text = _('Vous avez choisi le meilleur produit nutitionnelle')
            return render(
                request, 'store/resultats.html',
                {'data': data, 'best_product': best_product, 'text': text}
                )
        paginator = Paginator(best_product, 15)
        best_product = paginator.page(page) 
    except PageNotAnInteger:
        best_product = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)


    except (IndexError, exceptions.ObjectDoesNotExist, ValueError, AttributeError):
        send_text = _("Essayez un autre produit.")
        produit = query
        return render(request, 'store/home.html', {'text': send_text, 'produit': produit})

    print(best_product)
    context = { 
            'data': data[0], 
            'best_product': best_product,
            'filter': filter_grade,
            'filter1': filter_rating,
            'rating': filter_rating,
            }
    print(f"Les produits de meilleurs grade : {filter_grade}")
    return render(request, 'store/resultats.html', context )
 

@login_required(login_url='login')
def aliment(request):
    """Display all aliment favorite of user
    """
    favorite = Favorite.objects.filter(
        user=request.user).select_related('product_choice', 'product_favorite', 'user')
    rating = Rating.objects.all()

    
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
    print(favorite[0].product_favorite.pk)

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

        avg_rating = Rating.objects.filter(product_rating__id=product_id).aggregate(Avg('rating'))# moyenne du produit 
        try:
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
                'rating': avg_rating,
                'product_rating': product_rating,
                'user_rating': user_rating,
                'user_voting': user_voting,
                }
            
            dump = json.dumps(context)
            return HttpResponse(dump, content_type='application/json')


        except:
            print('toto')
            

            context = {
                'data': " Une erreure c'est produite"
            }
            dump = json.dumps(context)
            return HttpResponse(dump, content_type='application/json')


@login_required(login_url='login')
def filter(request, page=1):
    """Displays the results of the search for substitute products
    """


    global data
    # First logic section   
    best_product = []
    filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
    filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    grade_contains_query = request.GET.get('grade')
    categorie_contains_query = request.GET.get('categorie')
    rating_contains_query = request.GET.get('rating')

 
    # Seconde logic section

    print(f'grade = {grade_contains_query}')
    print(f'categorie = {categorie_contains_query}')
    print(f'rating = {rating_contains_query}')
    filter_product = []


    """ logic of seconde user search (get constum search with 3 fields ( grade, categorie, rating))
    """
    if rating_contains_query:
        print('choix 1-Utilisateur choisis recherche par note')
        if categorie_contains_query and grade_contains_query:  # If select categorie and grade  
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            categorie=categorie_contains_query, 
                                                            grade=grade_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)

        elif categorie_contains_query and grade_contains_query is None:  # If select categorie only 
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            categorie=categorie_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)

        elif categorie_contains_query is None and grade_contains_query:  # If select grade only 
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            grade=grade_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)

        else: # If not select the both
            filter_product = Product.objects.filter(rating__rating=rating_contains_query,)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)
                                                        
        filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
        filter_grade = ProductFilter(request.GET, queryset=filter_product)
        print((f'Nombre de produit trouves {len(filter_product)}'))

    elif categorie_contains_query or grade_contains_query:
        print('choix 2- Utilisateur choisis une recherche par grade ou par categorie')
        filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    else:
        print('choix 3- a faire ??? ')
    
    filter_qs = filter_grade.qs
    paginator = Paginator(filter_qs, 15)
    page = request.GET.get('page')
    print(page)
    try:
        filter_qs = paginator.page(page) 
    except PageNotAnInteger:
        filter_qs = paginator.page(1)
    except EmptyPage:
        filter_qs = paginator.page(paginator.num_pages)

    context = {
        'data': data, 
        'best_product': filter_qs,
        'filter': filter_grade,
        'filter1': filter_rating,
        'rating': filter_rating,
        }
    print(filter_grade)
    return render(request, 'store/filter.html', context )

# class filterListView(ListView):
#     model = Product
#     template_name = ('store/filter.html')
#     paginate_by = 15
#     context_object_name = 'best_product'

#     def get_queryset(request):
#         return Product.objects.all()