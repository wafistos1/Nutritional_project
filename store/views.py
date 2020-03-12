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
from django.db.models import Avg, Q
from django.core import exceptions, serializers
from .serializers import productSerializer
from .filters import ProductFilter, RatingFilter


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
    global data
    
    best_product = []
    filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
    filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    if request.GET.get('q') is not None:

        query = request.GET.get('q').capitalize()

        try:
            data = Product.objects.filter(name__contains=query).first()
            best_product = Product.objects.filter(
                categorie=data.categorie
                ).filter(grade__lt=data.grade).order_by("grade")
            filter_grade = ProductFilter(request.GET, queryset=best_product)
            print(best_product)
            context = {
                'data': data, 
                'best_product': filter_grade,
                'filter': filter_grade,
                'filter1': filter_rating,
                'rating': filter_rating,
                }
            print(filter_grade)
            return render(request, 'store/resultats.html', context )
    
            if  not best_product:
                text = _('Vous avez choisi le meilleur produit nutitionnelle')
                return render(
                    request, 'store/resultats.html',
                    {'data': data, 'best_product': best_product, 'text': text}
                    )
            paginator = Paginator(best_product, 15)
            best_product = paginator.page(page)
        except (IndexError, exceptions.ObjectDoesNotExist, ValueError, AttributeError):
            send_text = _("Essayez un autre produit.")
            produit = query
            return render(request, 'store/home.html', {'text': send_text, 'produit': produit})
        except EmptyPage:
            paginator = paginator.page(paginator.num_pages)
    
    grade_contains_query = request.GET.get('grade')
    categorie_contains_query = request.GET.get('categorie')
    rating_contains_query = request.GET.get('rating')

    print(f'grade = {grade_contains_query}')
    print(f'categorie = {categorie_contains_query}')
    print(f'rating = {rating_contains_query}')
    filter_product = []
    filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
    if rating_contains_query:
        print('choix 1 ')
        if categorie_contains_query and grade_contains_query:
            # filter_rate1 = Rating.objects.filter(rating=rating_contains_query)
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            categorie=categorie_contains_query, 
                                                            grade=grade_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)
        elif categorie_contains_query and grade_contains_query is None:
            # filter_rate1 = Rating.objects.filter(rating=rating_contains_query)
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            categorie=categorie_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)
        elif categorie_contains_query is None and grade_contains_query:
            #filter_rate1 = Rating.objects.filter(rating=rating_contains_query)
            filter_product = Product.objects.filter(rating__rating=rating_contains_query, 
                                                            grade=grade_contains_query)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)
        else:
            #filter_rate1 = Rating.objects.filter(rating=rating_contains_query)
            filter_product = Product.objects.filter(rating__rating=rating_contains_query,)
            filter_grade = ProductFilter(request.GET, queryset=filter_product)
                                                        
        filter_rating = RatingFilter(request.GET, queryset=Rating.objects.all())
        filter_grade = ProductFilter(request.GET, queryset=filter_product)
        print((f'Nombre de produit trouves {len(filter_product)}'))

    elif categorie_contains_query or grade_contains_query:
        print('choix 2')
        filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    else:
        print('choix 3')
    # best_product = Product.objects.filter(Q(grade=grade_contains_query) & Q(categorie=categorie_contains_query) )
    # filter_grade = ProductFilter(request.GET, queryset=Product.objects.all())
    # filter_note = RatingFilter(request.GET, )
    # filter_note = RatingFilter(request.GET, queryset=Rating.objects.all())



    # if rating_contains_query != '' and  query is not None:
    #     best = Product.objects.filter(grade=grade_contains_query, categorie=categorie_contains_query)
    # best_product = Rating.objects.filter(product_rating__in=best, rating=rating_contains_query)
    

    context = {
        'data': data, 
        'best_product': filter_grade,
        'filter': filter_grade,
        'filter1': filter_rating,
        'rating': filter_rating,
        }
    print(filter_grade)
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
def resultat(request):
    """Displays the results of the search for substitute products
    """
    if request.method == 'GET':
        grade = request.GET['value']
        grade = grade.lower()
        try:
            data = Product.objects.filter(name__contains=query).first()
            print(data.categorie.pk)
            best_product = Product.objects.filter(
                categorie=data.categorie.pk
                ).filter(grade__exact=grade)
            item = len(best_product)
            print(item)
        
        except (IndexError, exceptions.ObjectDoesNotExist, ValueError ):
            print('coucou')
            # send_text = _("Essayez un autre produit.")
            # produit = query
            # return render(request, 'store/home.html', {'text': send_text, 'produit': produit})
        best_serializer = productSerializer(best_product, many=True)
        data_serializer = productSerializer([data], many=True)
                
        context = {
            'best': best_serializer.data, 
            'data': data_serializer.data,
            'item': item
        }
        context = json.dumps(context)
  
        return HttpResponse(context, content_type='application/json')