import logging
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, RealEstatePropertyForm
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from django.db.models import Q, Avg, Min, Max

from .models import CustomUser, Notification, Product, Facture, Follow, ProductImage, RealEstateProperty
import unicodedata
from .ai_services.recommendation import ProductRecommender
from .ai_services.smart_search import SmartSearch
from .ai_services.price_analysis import PriceAnalyzer
from .filters import ProductFilter

# Create your views here.
''' =========== Authentication ========= '''
def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']  
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            
            roles_valides = ['admin','personnel', 'ecole', 'entreprise']

            if user.rôle == 'admin':
                return redirect('SuperAdmin')
            else:
                return redirect('home')

    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        try:
            form.full_clean()  # Utilisez full_clean pour déclencher toutes les validations du formulaire
        except ValidationError as e:
            for field, messages in e.message_dict.items():
                form.add_error(field, messages)

        if form.is_valid():
            # Sauvegarder l'utilisateur pour obtenir la clé primaire
            user = form.save()
            
            # Maintenant, vous pouvez définir les autres champs
            user.latitude = request.POST.get('latitude')
            user.longitude = request.POST.get('longitude')
            user.save()  # Sauvegarder à nouveau pour mettre à jour les champs

            # Connecter l'utilisateur
            user.backend = 'SunApp.backends.EmailBackend'
            login(request, user)

            # Rediriger vers le profil approprié selon le rôle
            user_role = user.rôle
            if user_role == 'admin':
                return render(request, 'auth/profile-admin.html')
            else:
                return render(request, 'auth/profile.html')

    else:
        form = CustomUserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        user = request.user
        
        pays = request.POST.get('pays')
        ville = request.POST.get('ville')
        quartier = request.POST.get('quartier')
        indicatif = request.POST.get('indicatif')
        phone = request.POST.get('phone')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        birthday = request.POST.get('birthday')
        
        # Mettre à jour les champs appropriés
        user.pays = pays
        user.ville = ville
        user.quartier = quartier
        user.indicatif_pays = indicatif
        user.number_phone = phone

        # Vérifier si les champs first_name et last_name sont fournis, sinon les définir sur None
        user.first_name = firstname if firstname else None
        user.last_name = lastname if lastname else None

        user.birthday = birthday

        user.save()

        # Déconnecter l'utilisateur après la mise à jour du profil
        logout(request)
        messages.success(request, 'Déconnecté👌🏾')
        return redirect('login')  # Rediriger vers la page de connexion après la mise à jour du profil

    user_role = request.user.rôle

    if user_role == 'admin':
        return render(request, 'auth/profile-admin.html')
    else:
        return render(request, 'auth/profile.html')

def log_out(request):
    # pass
    logout(request)
    messages.success(request, 'Déconnecté👌🏾')
    return redirect('login')

''' =========== User Pages ========= '''
def home(request):
    # Récupérer les filtres de la requête
    category_filter = request.GET.get('category', '')
    type_propriete_filter = request.GET.get('type_propriete', '')
    search_query = request.GET.get('search', '')

    # Requête de base pour les produits
    products_query = Product.objects.all()
    real_estate_query = RealEstateProperty.objects.all()

    # Filtrer par catégorie si spécifié
    if category_filter:
        # Filtrer uniquement les produits standards
        products_query = products_query.filter(category=category_filter)
        # Vider les biens immobiliers si un filtre de catégorie produit est actif
        real_estate_query = RealEstateProperty.objects.none()

    # Filtrer par type de propriété si spécifié
    if type_propriete_filter:
        # Filtrer uniquement les biens immobiliers
        real_estate_query = real_estate_query.filter(type_propriete=type_propriete_filter)
        # Vider les produits si un filtre de type de propriété est actif
        products_query = Product.objects.none()

    # Filtrer par recherche si spécifié
    if search_query:
        products_query = products_query.filter(
            Q(title__icontains=search_query) | 
            Q(contenu_post__icontains=search_query)
        )
        real_estate_query = real_estate_query.filter(
            Q(titre__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Combiner les résultats
    combined_results = list(products_query) + list(real_estate_query)

    # Trier par date de création (du plus récent au plus ancien)
    combined_results.sort(
        key=lambda x: x.date_creation_post if hasattr(x, 'date_creation_post') else x.date_creation, 
        reverse=True
    )

    # Pagination
    paginator = Paginator(combined_results, 10)  # 10 éléments par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Ajouter un attribut pour identifier le type
    for item in page_obj:
        item.item_type = 'Product' if isinstance(item, Product) else 'RealEstateProperty'

    context = {
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'Product': Product,
    }

    return render(request, 'users/pages/home.html', context)

@login_required
def boutique(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')
    
    # Filtrer les utilisateurs ayant le rôle "boutiques"
    boutiques = CustomUser.objects.filter(rôle='boutiques')

    # Vérifier si une recherche par nom d'utilisateur est effectuée
    query = request.GET.get('poste', '')
    if query:
        boutiques = boutiques.filter(username__icontains=query)

    # Normaliser les informations des boutiques pour le tri
    def normalize_boutique(boutique):
        return (
            normalize_string(boutique.pays or ''),
            normalize_string(boutique.ville or ''),
            normalize_string(boutique.quartier or '')
        )
    
    # Fonction de tri pour les boutiques
    def sorting_key(boutique):
        boutique_pays, boutique_ville, boutique_quartier = normalize_boutique(boutique)

        # Création de la clé de tri basée sur les critères définis
        return (
            not (boutique_pays == user_pays and boutique_ville == user_ville and boutique_quartier == user_quartier),
            not (boutique_pays == user_pays and boutique_ville == user_ville),
            not (boutique_pays == user_pays)
        )
    
    # Trier les boutiques en fonction de la logique définie
    boutiques = sorted(boutiques, key=sorting_key)

    return render(request, 'users/pages/boutique.html', {'boutiques': boutiques, 'query': query})


def super_marcher(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')
    
    # Filtrer les utilisateurs ayant le rôle "boutiques"
    supermarket = CustomUser.objects.filter(rôle='supermarket')

    # Vérifier si une recherche par nom d'utilisateur est effectuée
    query = request.GET.get('poste', '')
    if query:
        supermarket = supermarket.filter(username__icontains=query)

    
    def normalize_supermarket(supermarket):
        return (
            normalize_string(supermarket.pays or ''),
            normalize_string(supermarket.ville or ''),
            normalize_string(supermarket.quartier or '')
        )
    
    
    def sorting_key(supermarket):
        supermarket_pays, supermarket_ville, supermarket_quartier = normalize_supermarket(supermarket)

        # Création de la clé de tri basée sur les critères définis
        return (
            not (supermarket_pays == user_pays and supermarket_ville == user_ville and supermarket_quartier == user_quartier),
            not (supermarket_pays == user_pays and supermarket_ville == user_ville),
            not (supermarket_pays == user_pays)
        )
    
    
    supermarket = sorted(supermarket, key=sorting_key)
    return render(request, 'users/pages/super_marcher.html', {'supermarket': supermarket, 'query': query})

def superette(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')
    
    # Filtrer les utilisateurs ayant le rôle "boutiques"
    superette = CustomUser.objects.filter(rôle='superette')

    # Vérifier si une recherche par nom d'utilisateur est effectuée
    query = request.GET.get('poste', '')
    if query:
        superette = superette.filter(username__icontains=query)

    
    def normalize_superette(superette):
        return (
            normalize_string(superette.pays or ''),
            normalize_string(superette.ville or ''),
            normalize_string(superette.quartier or '')
        )
    
    
    def sorting_key(superette):
        superette_pays, superette_ville, superette_quartier = normalize_superette(superette)

        # Création de la clé de tri basée sur les critères définis
        return (
            not (superette_pays == user_pays and superette_ville == user_ville and superette_quartier == user_quartier),
            not (superette_pays == user_pays and superette_ville == user_ville),
            not (superette_pays == user_pays)
        )
    
    
    superette = sorted(superette, key=sorting_key)
    return render(request, 'users/pages/superette.html', {'superette': superette, 'query': query})

def particulier(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')
    
    # Filtrer les utilisateurs ayant le rôle "boutiques"
    particulier = CustomUser.objects.filter(rôle='particulier')

    # Vérifier si une recherche par nom d'utilisateur est effectuée
    query = request.GET.get('poste', '')
    if query:
        particulier = particulier.filter(username__icontains=query)

    
    def normalize_particulier(particulier):
        return (
            normalize_string(particulier.pays or ''),
            normalize_string(particulier.ville or ''),
            normalize_string(particulier.quartier or '')
        )
    
    
    def sorting_key(particulier):
        particulier_pays, particulier_ville, particulier_quartier = normalize_particulier(particulier)

        # Création de la clé de tri basée sur les critères définis
        return (
            not (particulier_pays == user_pays and particulier_ville == user_ville and particulier_quartier == user_quartier),
            not (particulier_pays == user_pays and particulier_ville == user_ville),
            not (particulier_pays == user_pays)
        )
    
    
    particulier = sorted(particulier, key=sorting_key)
    return render(request, 'users/pages/particulier.html', {'particulier': particulier, 'query': query})

def imobilier(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

    # Récupérer l'utilisateur connecté
    user = request.user
    
    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')
    
    # Filtrer les utilisateurs ayant le rôle "boutiques"
    imobilier = CustomUser.objects.filter(rôle='imobilier')

    # Vérifier si une recherche par nom d'utilisateur est effectuée
    query = request.GET.get('poste', '')
    if query:
        imobilier = imobilier.filter(username__icontains=query)

    
    def normalize_station(imobilier):
        return (
            normalize_string(imobilier.pays or ''),
            normalize_string(imobilier.ville or ''),
            normalize_string(imobilier.quartier or '')
        )
    
    
    def sorting_key(imobilier):
        imobilier_pays, imobilier_ville, imobilier_quartier = normalize_station(imobilier)

        # Création de la clé de tri basée sur les critères définis
        return (
            not (imobilier_pays == user_pays and imobilier_ville == user_ville and imobilier_quartier == user_quartier),
            not (imobilier_pays == user_pays and imobilier_ville == user_ville),
            not (imobilier_pays == user_pays)
        )
    
    
    imobilier = sorted(imobilier, key=sorting_key)
    return render(request, 'users/pages/imobilier.html', {'imobilier': imobilier, 'query': query})

def facture_users(request):
    # Fonction pour normaliser les chaînes de caractères (insensible aux majuscules, minuscules, accents)
    def normalize_string(s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()
    # Récupérer l'utilisateur connecté
    user = request.user

    # Normaliser les informations de l'utilisateur connecté
    user_pays = normalize_string(user.pays or '')
    user_ville = normalize_string(user.ville or '')
    user_quartier = normalize_string(user.quartier or '')

    # Filtrer les utilisateurs ayant le rôle "superette" et qui ont des factures publiques
    utilisateurs_publics = CustomUser.objects.filter(
        facture__is_public=True
    ).distinct()  # Utilisez distinct() pour éviter les doublons

    # Appliquer le filtre pour correspondre à la localisation de l'utilisateur
    utilisateurs_publics = [
        utilisateur for utilisateur in utilisateurs_publics
        if (
            normalize_string(utilisateur.pays or '') == user_pays and
            normalize_string(utilisateur.ville or '') == user_ville and
            normalize_string(utilisateur.quartier or '') == user_quartier
        )
    ]

    return render(request, 'users/pages/facture.html', {'utilisateurs_publics': utilisateurs_publics})
    
''' ========== Pages Notifications ================= '''
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')  # Récupérer les notifications de l'utilisateur
    return render(request, 'users/pages/notifications.html', {'notifications': user_notifications})

def notifications_view(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)

    has_new_notifications = notifications.filter(is_read=False).exists()

    return render(request, 'users/pages/notifications.html', {
        'notifications': notifications,
        'has_new_notifications': has_new_notifications
    })

def mark_notifications_as_read(request):
    if request.method == 'POST':
        # Vérifiez combien de notifications seront supprimées
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        logging.debug(f"Nombre de notifications non lues pour l'utilisateur {request.user}: {count}")
        
        # Supprimez les notifications
        Notification.objects.filter(user=request.user, is_read=False).delete()
        
        # Rediriger avec un message de succès
        messages.success(request, f"{count} notifications supprimées.")
    return redirect('facture_users')

def check_notifications(request):
    if request.user.is_authenticated:
        has_new_notifications = Notification.objects.filter(user=request.user, is_read=False).exists()
        return JsonResponse({'has_new_notifications': has_new_notifications})
    return JsonResponse({'has_new_notifications': False})


''' =========== Admins Pages ========= '''
@login_required
def SuperAdmin(request):
    return render(request, 'admins/dashboard.html')

''' ========== Les Formulaires ================= '''
@login_required
def create_product(request):
    # Définition des catégories de produits
    PRODUCT_CATEGORIES = [
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

    if request.method == 'POST':
        # Récupérer les données du formulaire
        title = request.POST.get('nom_produit')
        prix = request.POST.get('prix')
        description = request.POST.get('description')
        category = request.POST.get('category')
        images = request.FILES.getlist('images')  # Récupérer toutes les images

        # Créer un nouveau produit
        product = Product.objects.create(
            user=request.user,
            title=title,
            prix=prix,
            contenu_post=description,
            category=category
        )
        
        # Enregistrer les images
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        
        # Redirection vers la page d'accueil après succès
        return redirect('home')

    # Si la méthode est GET, afficher le formulaire
    return render(request, 'formulaires/product.html', {
        'product_categories': PRODUCT_CATEGORIES
    })

def create_immo(request):
    # Vérifier que seuls les utilisateurs avec le rôle immobilier peuvent poster
    if request.user.rôle not in ['immobilier', 'imobilier']:
        messages.error(request, "Vous n'avez pas les permissions nécessaires.")
        return redirect('home')

    if request.method == 'POST':
        form = RealEstatePropertyForm(request.POST, request.FILES)
        if form.is_valid():
            real_estate_property = form.save(user=request.user)
            messages.success(request, "Votre bien immobilier a été posté avec succès.")
            return redirect('home')
        else:
            messages.error(request, "Il y a des erreurs dans le formulaire.")
    else:
        form = RealEstatePropertyForm()

    return render(request, 'formulaires/immo.html', {
        'form': form,
        'title': 'Poster un bien immobilier'
    })

def facture(request):
    factures = Facture.objects.filter(user=request.user)
    
    # Vérifier si toutes les factures sont partagées
    all_shared = factures.filter(is_public=False).count() == 0
    
    if request.method == "POST":
        if 'share_all' in request.POST:
            # Partager toutes les factures de l'utilisateur
            factures.update(is_public=True)
            
            # Envoyer la notification après le partage
            users_with_public_invoices = CustomUser.objects.filter(
                pays=request.user.pays,
                quartier=request.user.quartier,
                ville=request.user.ville
            )
            # Créer une notification pour chaque utilisateur
            for user in users_with_public_invoices:
                Notification.objects.create(user=user, message=f"{request.user.username} a partagé ses factures.")

        elif 'unshare_all' in request.POST:
            # Ne plus partager toutes les factures de l'utilisateur
            factures.update(is_public=False)

        return redirect('facture')

    return render(request, 'formulaires/facture.html', {'factures': factures, 'all_shared': all_shared})


def public_factures(request):
    factures = Facture.objects.filter(is_public=True)
    return render(request, 'formulaires/public_facture.html', {'factures': factures})

@login_required
def product_detail(request, product_id):
    # Récupérer le produit avec toutes ses images
    product = get_object_or_404(Product, id=product_id)
    product_images = product.images.all()
    
    # Récupérer des produits similaires dans la même catégorie
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:6]  # 6 produits similaires max
    
    context = {
        'product': product,
        'product_images': product_images,
        'similar_products': similar_products
    }
    
    return render(request, 'Details/details_product.html', context)

def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    products = Product.objects.filter(user=user)
    
    # Vérifier si l'utilisateur connecté suit déjà cet utilisateur
    is_following = False
    if request.user.is_authenticated and request.user.rôle == 'acheteur':
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    return render(request, 'Details/details_user.html', {
        'user': user, 
        'products': products,
        'is_following': is_following
    })

@login_required
def toggle_follow(request, user_id):
    # Vérifier que l'utilisateur connecté a le rôle d'acheteur
    if request.user.rôle != 'acheteur':
        messages.error(request, "Vous n'êtes pas autorisé à suivre des utilisateurs.")
        return redirect('user_detail', user_id=user_id)

    followed_user = get_object_or_404(CustomUser, pk=user_id)
    
    # Ne pas permettre de se suivre soi-même
    if request.user == followed_user:
        messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect('user_detail', user_id=user_id)

    # Vérifier si l'utilisateur est déjà suivi
    existing_follow = Follow.objects.filter(follower=request.user, followed=followed_user)
    
    if existing_follow.exists():
        # Déjà suivi, donc on arrête de suivre
        existing_follow.delete()
        messages.success(request, f"Vous avez arrêté de suivre {followed_user.username}.")
    else:
        # Commencer à suivre
        Follow.objects.create(follower=request.user, followed=followed_user)
        messages.success(request, f"Vous suivez maintenant {followed_user.username}.")

    return redirect('user_detail', user_id=user_id)

def followed_users(request):
    # Vérifier que l'utilisateur est connecté et a le rôle d'acheteur
    if not request.user.is_authenticated or request.user.rôle != 'acheteur':
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('home')

    # Récupérer tous les utilisateurs suivis
    followed_users = CustomUser.objects.filter(
        followers__follower=request.user
    ).distinct()

    return render(request, 'Details/followed_users.html', {
        'followed_users': followed_users
    })

def facture_detail(request, id):
    # Récupérer l'utilisateur associé à l'ID
    user = get_object_or_404(CustomUser, id=id)
    
    # Récupérer toutes les factures de cet utilisateur
    factures = Facture.objects.filter(user=user, is_public=True)  # Optionnel: filtre pour les factures publiques
    
    return render(request, 'Details/public_facture.html', {'factures': factures, 'user': user})

@login_required
def real_estate_detail(request, real_estate_id):
    # Récupérer le bien immobilier avec toutes ses images
    real_estate_property = get_object_or_404(RealEstateProperty, id=real_estate_id)
    property_images = real_estate_property.property_images.all()
    
    # Récupérer des biens immobiliers similaires
    similar_properties = RealEstateProperty.objects.filter(
        type_propriete=real_estate_property.type_propriete,
        ville=real_estate_property.ville
    ).exclude(id=real_estate_property.id)[:6]  # 6 biens similaires max
    
    context = {
        'property': real_estate_property,
        'property_images': property_images,
        'similar_properties': similar_properties
    }
    
    return render(request, 'Details/details_real_estate.html', context)