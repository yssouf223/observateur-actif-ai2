import os
import random
from google import genai

def choisir_sujet():
    """Demande à Gemini d'inventer un sujet inédit sur l'Afrique."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    # On donne des thèmes variés pour ne pas tourner en rond
    themes = [
        "un mythe ou une légende oubliée", 
        "un lieu mystérieux ou un monument étrange", 
        "un personnage historique énigmatique", 
        "une créature ou un esprit du folklore", 
        "un rituel ou une tradition insolite",
        "un trésor perdu ou une cité disparue"
    ]
    theme = random.choice(themes)
    
    prompt = f"""Tu es un chercheur spécialiste des mystères et de l'insolite en Afrique.
Trouve un sujet fascinant, méconnu et mystérieux concernant {theme} en Afrique.
Donne-moi UNIQUEMENT le nom de ce sujet, sous forme d'une phrase courte de 5 à 10 mots (en français).
Ne mets pas de ponctuation, ni de guillemets, ni de texte avant ou après.
Exemple : Le mystère des cercueils suspendus de Sagada (non, ça c'est en Asie, trouve en Afrique)
Exemple : La légende des mines du roi Salomon en Éthiopie
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        sujet = response.text.strip()
        # On nettoie au cas où l'IA aurait mis des guillemets
        sujet = sujet.replace('"', '').replace("'", "").replace(".", "")
        return sujet
    except Exception as e:
        print(f"⚠️ Erreur lors de la recherche du sujet : {e}")
        # En cas de problème, on utilise un sujet de secours
        return "Le mystère non résolu des gravures rupestres du Tassili n'Ajjer"