from rest_framework import serializers
from .models import CustomUser, Product, Facture

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'rôle', 'pays', 'ville', 'quartier']
        read_only_fields = ['id']

class ProductSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'user', 'title', 'prix', 'contenu_post', 'image', 
                 'category', 'pays', 'ville', 'quartier', 'created_at']
        read_only_fields = ['id', 'created_at']

class FactureSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = Facture
        fields = ['id', 'user', 'product', 'quantity', 'is_public', 'created_at']
        read_only_fields = ['id', 'created_at'] 