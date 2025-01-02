from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import RealEstateProperty, ProductImage

TYPE_PROPRIETE_CHOICES = [
    ('appartement', 'Appartement'),
    ('maison', 'Maison'),
    ('terrain', 'Terrain'),
    ('bureau', 'Bureau'),
    ('entrepot', 'Entrepôt')
]

class CustomUserCreationForm(UserCreationForm):
    rôle = forms.ChoiceField(choices=get_user_model().ROLES, initial='acheteur', widget=forms.Select(attrs={'autocomplete': 'off'}))
    genre = forms.ChoiceField(choices=get_user_model().GENRE, widget=forms.Select(attrs={'autocomplete': 'off'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    nom_boutique = forms.CharField(widget=forms.TextInput(attrs={'autocomplete': 'off'}), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))
    
    class Meta:
        model = get_user_model()
        fields = ('rôle', 'genre', 'username', 'nom_boutique', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        rôle = cleaned_data.get('rôle')
        nom_boutique = cleaned_data.get('nom_boutique')
        
        # Validate username length if it is not None
        if username is not None and len(username) > 150:
            self.add_error('username', "Le nom d'utilisateur ne peut pas dépasser 150 caractères.")
        
        # Validate email uniqueness if it is not None
        if email is not None and get_user_model().objects.filter(email=email).exists():
            self.add_error('email', "Un compte avec cette adresse e-mail existe déjà.")
        
        # Validate passwords match if both are not None
        if password1 is not None and password2 is not None and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")

        # Validate nom_boutique requirement based on role
        if rôle != 'acheteur' and not nom_boutique:
            self.add_error('nom_boutique', "Le nom de la boutique est obligatoire pour ce rôle")
    
        return cleaned_data


class RealEstatePropertyForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.FileInput(), 
        required=False, 
        help_text="Vous pouvez télécharger plusieurs images"
    )

    class Meta:
        model = RealEstateProperty
        fields = [
            'titre', 'description', 'prix', 
            'type_propriete', 'type_transaction', 
            'superficie', 'nombre_chambres', 'nombre_salles_bain',
            'adresse', 'ville', 'quartier', 
            'annee_construction', 'diagnostics_energetiques',
            # Nouveaux champs
            'nombre_etages', 'etage', 
            'superficie_terrain', 'superficie_local', 
            'type_activite', 'constructible'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'required': 'required'}),
            'diagnostics_energetiques': forms.Textarea(attrs={'rows': 3, 'required': False}),
            'type_transaction': forms.Select(attrs={'class': 'field', 'required': 'required'}),
            'type_propriete': forms.Select(choices=TYPE_PROPRIETE_CHOICES, attrs={'class': 'field', 'required': 'required'}),
            'constructible': forms.Select(choices=[(True, 'Oui'), (False, 'Non')], attrs={'class': 'field'})
        }
        error_messages = {
            'titre': {
                'required': 'Le titre du bien est obligatoire.',
                'max_length': 'Le titre ne peut pas dépasser 200 caractères.'
            },
            'description': {
                'required': 'La description du bien est obligatoire.',
            },
            'prix': {
                'required': 'Le prix est obligatoire.',
                'min_value': 'Le prix doit être un nombre positif.'
            },
            'type_propriete': {
                'required': 'Le type de propriété est obligatoire.',
            },
            'type_transaction': {
                'required': 'Le type de transaction est obligatoire.',
            },
            'superficie': {
                'required': 'La superficie est obligatoire.',
                'min_value': 'La superficie doit être un nombre positif.'
            },
            'adresse': {
                'required': 'L\'adresse est obligatoire.',
                'max_length': 'L\'adresse ne peut pas dépasser 300 caractères.'
            },
            'ville': {
                'required': 'La ville est obligatoire.',
                'max_length': 'Le nom de la ville ne peut pas dépasser 100 caractères.'
            },
            'quartier': {
                'required': 'Le quartier est obligatoire.',
                'max_length': 'Le nom du quartier ne peut pas dépasser 100 caractères.'
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Validation supplémentaire spécifique aux types de propriété
        type_propriete = cleaned_data.get('type_propriete')
        
        # Validation de la superficie
        superficie = cleaned_data.get('superficie')
        superficie_terrain = cleaned_data.get('superficie_terrain')
        
        # Selon le type de propriété, on ajuste la validation de la superficie
        if type_propriete == 'maison':
            # Pour une maison, on prend la superficie du terrain
            if not superficie_terrain or superficie_terrain <= 0:
                self.add_error('superficie_terrain', 'La superficie du terrain est obligatoire pour une maison.')
            
            # La superficie générale est optionnelle pour une maison
            if superficie and superficie <= 0:
                self.add_error('superficie', 'La superficie doit être un nombre positif.')
        
        elif type_propriete == 'appartement':
            # Pour un appartement, la superficie générale est obligatoire
            if not superficie or superficie <= 0:
                self.add_error('superficie', 'La superficie est obligatoire pour un appartement.')
        
        elif type_propriete == 'terrain':
            # Pour un terrain, la superficie générale est obligatoire
            if not superficie or superficie <= 0:
                self.add_error('superficie', 'La superficie est obligatoire pour un terrain.')
        
        elif type_propriete == 'local_commercial':
            # Pour un local commercial, la superficie générale est obligatoire
            if not superficie or superficie <= 0:
                self.add_error('superficie', 'La superficie est obligatoire pour un local commercial.')
        
        return cleaned_data

    def save(self, commit=True, user=None):
        # Sauvegarder l'instance de RealEstateProperty
        instance = super().save(commit=False)
        
        # Ajouter le propriétaire si un utilisateur est fourni
        if user:
            instance.proprietaire = user
        
        # Sauvegarder l'instance si commit est True
        if commit:
            instance.save()
        
        # Gestion des images
        images = self.files.getlist('images')
        if images:
            # Créer une image pour chaque fichier téléchargé
            for image_file in images:
                ProductImage.objects.create(
                    real_estate_property=instance,
                    image=image_file
                )
        
        return instance