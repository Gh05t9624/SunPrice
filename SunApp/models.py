from django.db import models
from django.contrib.auth.models import AbstractUser as BaseAbstractUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericRelation

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(BaseAbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('acheteur', 'Acheteur'),
        ('particulier', 'Particulier'),
        ('boutiques', 'Boutique'),
        ('supermarket', 'Super Marché'),
        ('imobilier', 'Agent Immobilier'),
    ]
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    banner_image = models.ImageField(upload_to='banner_images/', null=True, blank=True)
    GENRE = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
    ]
    SITUATION_MATRIMONIALE = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
    ]
    nom_boutique = models.CharField(max_length=255, null=True, blank=True)
    marque_dispositif = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    quartier = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    indicatif_pays = models.CharField(max_length=15, null=True, blank=True)
    number_phone = models.CharField(max_length=15, null=True, blank=True)
    rôle = models.CharField(max_length=255, choices=ROLES, default='acheteur')
    genre = models.CharField(max_length=255, choices=GENRE, default='homme')
    situation_matrimoniale = models.CharField(max_length=20, choices=SITUATION_MATRIMONIALE, default='celibataire')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username if self.username else 'Utilisateur sans nom'

    class Meta:
        # Vous pouvez ajouter ici des contraintes spécifiques si nécessaire
        unique_together = ('email',)  # Conserver l'unicité de l'email si désiré

class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name_plural = 'Follows'

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    
class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, related_name='product_images')
    real_estate_property = models.ForeignKey('RealEstateProperty', on_delete=models.CASCADE, null=True, blank=True, related_name='property_images')
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    
    def __str__(self):
        if self.product:
            return f"Image for {self.product.title}"
        elif self.real_estate_property:
            return f"Image for {self.real_estate_property.titre}"
        return "Unassigned Image"

class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('electronics', 'Électronique'),
        ('fashion', 'Mode et Vêtements'),
        ('beauty_health', 'Beauté et Santé'),
        ('food_drink', 'Alimentation et Boissons'),
        ('sports_leisure', 'Sport et Loisirs'),
        ('books_media', 'Livres et Médias'),
        ('toys_kids', 'Jouets et Enfants'),
        ('automotive_tools', 'Automobile et Outils'),
        ('pets', 'Animaux'),
        ('services', 'Services et Abonnements'),
        ('special_offers', 'Offres spéciales / Promotions'),
    ]

    title = models.CharField(max_length=255)
    contenu_post = models.TextField()
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        default='electronics',  # Valeur par défaut
        null=False,  # Ne peut pas être null
        blank=False  # Ne peut pas être vide
    )
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation_post = models.DateTimeField(auto_now_add=True)
    # ... autres champs ...

    def get_images(self):
        return self.product_images.all()

    def get_first_image(self):
        first_image = self.product_images.first()
        return first_image.image if first_image else None

    def migrate_images_to_product_images(self):
        """
        Migre l'ancien champ image vers le nouveau modèle ProductImage
        """
        if hasattr(self, 'image') and self.image:
            ProductImage.objects.create(
                product=self,
                image=self.image
            )
            # Optionnel : supprimez l'ancien champ image si nécessaire
            # self.image.delete()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Migrer les images uniquement lors de la création initiale
        if is_new:
            self.migrate_images_to_product_images()

    @classmethod
    def product_categories(cls):
        categories = list(cls.CATEGORY_CHOICES.copy())
        return tuple(categories)

    def __str__(self):
        return self.title

class Facture(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_public = models.BooleanField(default=False) 
    date_creation = models.DateTimeField(auto_now_add=True)
    
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Assurez-vous que ce champ existe

    def __str__(self):
        return self.message

class RealEstateProperty(models.Model):
    TYPE_PROPRIETE_CHOICES = [
        ('appartement', 'Appartement'),
        ('maison', 'Maison'),
        ('terrain', 'Terrain'),
        ('bureau', 'Bureau'),
        ('entrepot', 'Entrepôt')
    ]
    TRANSACTION_TYPES = [
        ('vente', 'Vente'),
        ('location', 'Location'),
        ('location-vente', 'Location-Vente'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Caractéristiques spécifiques à l'immobilier
    type_propriete = models.CharField(max_length=20, choices=TYPE_PROPRIETE_CHOICES)
    type_transaction = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    superficie = models.FloatField(help_text="Superficie en m²")
    nombre_chambres = models.IntegerField(null=True, blank=True)
    nombre_salles_bain = models.IntegerField(null=True, blank=True)
    
    # Nouveaux champs pour différents types de propriété
    nombre_etages = models.IntegerField(null=True, blank=True, help_text="Nombre d'étages (pour maisons)")
    etage = models.IntegerField(null=True, blank=True, help_text="Étage (pour appartements)")
    superficie_terrain = models.FloatField(null=True, blank=True, help_text="Superficie du terrain (pour maisons)")
    superficie_local = models.FloatField(null=True, blank=True, help_text="Superficie du local (pour locaux commerciaux)")
    type_activite = models.CharField(max_length=100, null=True, blank=True, help_text="Type d'activité (pour locaux commerciaux)")
    constructible = models.BooleanField(null=True, blank=True, help_text="Terrain constructible (pour terrains)")
    
    # Localisation
    adresse = models.CharField(max_length=300)
    ville = models.CharField(max_length=100)
    quartier = models.CharField(max_length=100)
    
    # Caractéristiques supplémentaires
    annee_construction = models.IntegerField(null=True, blank=True)
    diagnostics_energetiques = models.TextField(null=True, blank=True)
    
    # Relation avec l'utilisateur
    proprietaire = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='proprietes')
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def get_first_image(self):
        first_image = self.property_images.first()
        return first_image.image if first_image else None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} - {self.type_propriete} à {self.ville}"

    class Meta:
        verbose_name = "Bien Immobilier"
        verbose_name_plural = "Biens Immobiliers"
        ordering = ['-date_creation']