from django.db import models
from django.contrib.auth.models import AbstractUser as BaseAbstractUser, BaseUserManager

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
        ('boutiques', 'Boutiques'),
        ('supermarket', 'Super-Marché'),
        ('imobilier', 'Imobilier'),
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


    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Électronique'),
        ('fashion', 'Mode et Vêtements'),
        ('home_garden', 'Maison et Jardin'),
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
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='electronics')
    pays = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    quartier = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=0)
    contenu_post = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    session_info = models.CharField(max_length=255, null=True, blank=True)
    date_creation_post = models.DateTimeField(auto_now_add=True)
    
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