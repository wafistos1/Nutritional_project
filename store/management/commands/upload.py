from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from store.models import Product, Categorie
import requests

class Command(BaseCommand):
    help = 'Uplaod data from OpenFactFood API'
    # def add_arguments(self, parser):
    #     parser.add_arguments('upload', type=str, help='upload data from OpenFactFood API')
    
    def handle(self, *args, **Kwargs):
        # Bit of logic to upload data
        
        """Loads the API data into a Json file and returns it
        """
        list_categories = [
            'Boissons',
            'Produits laitiers',
            'Biscuits',
            'Petit-déjeuners',
            'Chocolats',
            'Salade',
            ]

        for index in list_categories:

            # Insert data in Product table
            # The loop that inserts the data into my tables
            api_search = 'https://world.openfoodfacts.org/cgi/search.pl?/get'
            payload = {
            'search_terms': '',
            'json': 1,
            'page_size': 1000,
            'page': 1,
            'categories': index,
                }
            json_data = requests.get(api_search, params=payload).json()
            taille = len(json_data['products'])
            print(f'{taille} Produits trouvés dans la catégorie {index}')

            # The loop that inserts the data into my tables
            for i in range(taille):
                try:
                    name = json_data['products'][i]['product_name']
                    grade = json_data['products'][i]['nutrition_grades_tags'][0]
                    image1 = json_data['products'][i]['image_front_url']
                    igredient_text = json_data['products'][i]['ingredients_text']
                    image_nutrition_url = json_data['products'][i]['image_nutrition_url']
                    url = json_data['products'][i]['url']
                    
                    categorie = index

                    categorie_ins, created = Categorie.objects.get_or_create(name=categorie)

                    product = Product.objects.get_or_create(
                        name=name,
                        grade=grade,
                        images=image1,
                        categorie=categorie_ins,
                        detail_igredient=igredient_text,
                        url=url,
                        detail_nutrition_url=image_nutrition_url,
                        )
                except(KeyError, TypeError) as error:
                    continue
                except IntegrityError as errorif:
                    continue

        
        self.stdout.write(self.style.SUCCESS('upload data done'))