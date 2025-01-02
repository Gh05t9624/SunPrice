import os
import django

# Configurer les paramètres de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SunPrice.settings')
django.setup()

# Importer les modèles
from SunApp.models import Product, RealEstateProperty, ProductImage

# Compter les enregistrements
print(f"Nombre de produits : {Product.objects.count()}")
print(f"Nombre de biens immobiliers : {RealEstateProperty.objects.count()}")
print(f"Nombre d'images : {ProductImage.objects.count()}")
