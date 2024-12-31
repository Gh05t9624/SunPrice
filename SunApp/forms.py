from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


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