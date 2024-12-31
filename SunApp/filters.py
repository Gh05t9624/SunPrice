import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=Product.CATEGORY_CHOICES)
    min_price = django_filters.NumberFilter(field_name="prix", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="prix", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price'] 