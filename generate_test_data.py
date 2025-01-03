import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SunPrice.settings')
django.setup()

from SunApp.models import CustomUser, Product

def generate_test_products(user):
    # Catégories disponibles
    categories = [
        'electronics', 'fashion', 'beauty_health', 
        'food_drink', 'sports_leisure', 'books_media'
    ]
    
    # Générer des produits sur les 6 derniers mois
    for month in range(6):
        for _ in range(random.randint(3, 10)):
            Product.objects.create(
                user=user,
                title=f"Produit Test {_}",
                contenu_post="Produit généré automatiquement pour test",
                category=random.choice(categories),
                prix=round(random.uniform(1000, 50000), 2),
                date_creation_post=timezone.now() - timedelta(days=month*30)
            )

def main():
    # Récupérer un utilisateur existant (remplacez par votre logique de sélection)
    user = CustomUser.objects.filter(rôle='boutiques').first()
    
    if not user:
        print("Aucun utilisateur trouvé. Créez un utilisateur d'abord.")
        return
    
    # Supprimer les produits existants
    Product.objects.filter(user=user).delete()
    
    # Générer de nouveaux produits
    generate_test_products(user)
    
    print(f"Généré des produits de test pour l'utilisateur {user.username}")

if __name__ == '__main__':
    main()
