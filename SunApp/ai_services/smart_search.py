from django.db.models import Q
from ..models import Product
import logging

class SmartSearch:
    def search(self, query):
        # Recherche simple sans NLTK
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(contenu_post__icontains=query)
        )
        logging.debug(f"Recherche pour '{query}' a retourné {products.count()} produits.")
        return products 