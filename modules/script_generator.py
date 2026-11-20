import os
import json
from google import genai
from google.genai import types

def generer_script(sujet):
    """Génère un script captivant pour un Short à partir d'un sujet."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    prompt = f"""Tu es un scénariste pour une chaîne YouTube de mystères et d'histoires insolites africaines nommée "Observateur Actif".
    Écris un script de 60 secondes maximum sur le sujet suivant : "{sujet}".
    Le script doit être captivant, avec une accroche forte dès les premières secondes, un développement intrigant et une chute mémorable.
    Il doit être écrit pour être raconté à l'oral, avec un ton mystérieux et engageant.
    Fournis la réponse UNIQUEMENT sous la forme d'un objet JSON valide, avec la structure exacte suivante :
    {{
        "titre": "Un titre accrocheur pour la vidéo (max 100 caractères)",
        "script": "Le texte complet du script à raconter",
        "mots_cles_visuels": ["une liste de 5 à 7 mots-clés en anglais pour rechercher des images d'illustration sur Pexels"]
    }}
    """
    
    # Configuration pour forcer une sortie JSON
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    # Le SDK Gemini peut directement parser la réponse JSON
    script_data = json.loads(response.text)
    return script_data