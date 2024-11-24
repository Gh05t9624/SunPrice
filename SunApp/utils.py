# utils.py
import re

def obtenir_marque_dispositif(request):
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    
    if 'iphone' in user_agent:
        marque = 'iPhone'
        modele_match = re.search(r'iphone (\w+)', user_agent)
        modele = modele_match.group(1) if modele_match else 'Inconnu'
    elif 'ipad' in user_agent:
        marque = 'iPad'
        modele_match = re.search(r'ipad (\w+)', user_agent)
        modele = modele_match.group(1) if modele_match else 'Inconnu'
    elif 'android' in user_agent:
        marque = 'Android'
        modele_match = re.search(r'\bandroid [\w\s]+\b', user_agent)
        modele = modele_match.group() if modele_match else 'Inconnu'
    elif 'windows phone' in user_agent:
        marque = 'Windows Phone'
        modele_match = re.search(r'windows phone (\w+)', user_agent)
        modele = modele_match.group(1) if modele_match else 'Inconnu'
    elif 'macintosh' in user_agent or 'mac os' in user_agent:
        marque = 'Mac'
        modele = 'Inconnu'  # Mac n'a pas de modèle spécifique dans l'en-tête User-Agent
    elif 'windows' in user_agent:
        marque = 'Windows'
        modele = 'Inconnu'  # Windows n'a pas de modèle spécifique dans l'en-tête User-Agent
    elif 'linux' in user_agent:
        marque = 'Linux'
        modele = 'Inconnu'  # Linux n'a pas de modèle spécifique dans l'en-tête User-Agent
    else:
        marque = 'Inconnu'
        modele = 'Inconnu'

    return marque, modele
