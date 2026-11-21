import os
import json
import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError

def generer_script(sujet):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    prompt = f"""Tu es un scénariste pour une chaîne YouTube de mystères et d'histoires insolites africaines nommée "Observateur Actif".
Écris un script de 50 secondes maximum sur le sujet suivant : "{sujet}".
Le script doit être captivant, avec une accroche forte dès les premières secondes, un développement intrigant et une chute mémorable.
Il doit être écrit pour être raconté à l'oral, avec un ton mystérieux et engageant.
Fournis la réponse UNIQUEMENT sous la forme d'un objet JSON valide, avec la structure exacte suivante :
{{
    "titre": "Un titre accrocheur pour la vidéo (max 100 caractères)",
    "script": "Le texte complet du script à raconter",
    "mots_cles_visuels": ["mot1", "mot2", "mot3", "mot4", "mot5", "mot6"] (Donne exactement 6 mots-clés en anglais, très descriptifs)
}}
"""

    max_retries = 4
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return json.loads(response.text)
            
        except ServerError as e:
            print(f"⚠️ Serveur Gemini surchargé (Essai {attempt + 1}/{max_retries}). Attente de 15 secondes...")
            if attempt == max_retries - 1:
                print("❌ Abandon après plusieurs tentatives. Réessaie plus tard.")
                raise e
            time.sleep(15) # On attend 15 secondes avant de réessayer