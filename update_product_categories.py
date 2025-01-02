from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SunPrice.settings')
get_wsgi_application()

from SunApp.models import Product

def update_categories():
    # Liste des catégories à supprimer
    categories_to_remove = ['home_garden']
    
    # Récupérer les produits avec ces catégories
    products_to_update = Product.objects.filter(category__in=categories_to_remove)
    
    print(f"Nombre de produits à mettre à jour : {products_to_update.count()}")
    
    # Mettre à jour avec une catégorie par défaut
    products_to_update.update(category='electronics')
    
    print("Mise à jour des catégories terminée.")

if __name__ == '__main__':
    update_categories()
