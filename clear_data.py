import os
import django

# Configurer les paramètres de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SunPrice.settings')
django.setup()

# Importer les modèles
from SunApp.models import Product, RealEstateProperty, ProductImage

# Supprimer tous les produits
Product.objects.all().delete()

# Supprimer tous les biens immobiliers
RealEstateProperty.objects.all().delete()

# Supprimer toutes les images
ProductImage.objects.all().delete()

print("Tous les produits, biens immobiliers et images ont été supprimés.")
