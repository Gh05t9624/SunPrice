from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CustomUserSerializer, ProductSerializer, FactureSerializer
from .models import CustomUser, Product, Facture

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email', 'pays', 'ville', 'quartier']
    filterset_fields = ['rôle', 'pays', 'ville']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        user = self.get_object()
        products = Product.objects.filter(user=user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'contenu_post']
    filterset_fields = ['category', 'pays', 'ville', 'quartier']
    ordering_fields = ['prix', 'created_at']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FactureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FactureSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_public']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Facture.objects.all()
        return Facture.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 