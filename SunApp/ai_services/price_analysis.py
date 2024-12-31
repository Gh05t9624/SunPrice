import pandas as pd
from sklearn.cluster import KMeans
from ..models import Product

class PriceAnalyzer:
    def analyze_price_trends(self, category=None):
        # Récupérer les produits
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)
            
        # Créer un DataFrame
        df = pd.DataFrame(list(products.values('prix', 'date_creation_post', 'category')))
        
        # Analyser les tendances de prix
        trends = df.groupby('category')['prix'].agg(['mean', 'min', 'max']).round(2)
        
        # Identifier les clusters de prix
        kmeans = KMeans(n_clusters=3)
        df['price_cluster'] = kmeans.fit_predict(df[['prix']])
        
        return {
            'trends': trends.to_dict(),
            'clusters': df.groupby('price_cluster')['prix'].agg(['mean', 'count']).to_dict()
        } 