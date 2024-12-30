import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import Product, Facture

class ProductRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def get_product_recommendations(self, user, n_recommendations=5):
        # Récupérer l'historique des achats de l'utilisateur
        user_purchases = Facture.objects.filter(user=user).values_list('product__id', flat=True)
        
        # Récupérer tous les produits
        products = Product.objects.all()
        
        # Créer un DataFrame avec les caractéristiques des produits
        product_data = []
        for product in products:
            product_data.append({
                'id': product.id,
                'title': product.title,
                'category': product.category,
                'description': product.contenu_post,
                'prix': product.prix
            })
        
        df = pd.DataFrame(product_data)
        
        # Créer une représentation textuelle pour chaque produit
        df['features'] = df['title'] + ' ' + df['category'] + ' ' + df['description']
        
        # Calculer la similarité entre les produits
        tfidf_matrix = self.vectorizer.fit_transform(df['features'])
        cosine_sim = cosine_similarity(tfidf_matrix)
        
        # Trouver les produits similaires à ceux achetés par l'utilisateur
        similar_products = []
        for product_id in user_purchases:
            idx = df[df['id'] == product_id].index[0]
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:n_recommendations+1]
            product_indices = [i[0] for i in sim_scores]
            similar_products.extend(df.iloc[product_indices]['id'].tolist())
        
        return Product.objects.filter(id__in=similar_products) 