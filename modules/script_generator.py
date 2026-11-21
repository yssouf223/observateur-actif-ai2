import os
import json
import time
import httpx
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

# Liste des modèles à essayer dans l'ordre (du plus récent au plus ancien)
MODELES = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
]

def generer_script(sujet):
    """Génère un script en essayant plusieurs modèles Gemini avec gestion des erreurs."""
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

    derniere_erreur = None

    for modele in MODELES:
        for attempt in range(3):  # 3 tentatives par modèle
            try:
                print(f"🤖 Essai avec le modèle : {modele} (Tentative {attempt + 1}/3)")
                response = client.models.generate_content(
                    model=modele,
                    contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json"),
                )
                print(f"✅ Script généré avec succès via {modele} !")
                return json.loads(response.text)

            except ClientError as e:
                # Erreur 404 : modèle non trouvé, on passe immédiatement au suivant
                if "404" in str(e) or "NOT_FOUND" in str(e):
                    print(f"⚠️ Le modèle {modele} n'est pas disponible. On passe au suivant.")
                    derniere_erreur = e
                    break  # On sort de la boucle des tentatives pour ce modèle

                # Autres erreurs client (ex: 429 quota) : on attend un peu
                print(f"⚠️ Erreur client avec {modele} : {e}")
                derniere_erreur = e
                if attempt < 2:
                    time.sleep(20)

            except (ServerError, httpx.RemoteProtocolError, httpx.TimeoutException) as e:
                # Erreur serveur ou réseau : on attend et on réessaie
                print(f"⚠️ Problème réseau/serveur avec {modele} (Tentative {attempt + 1}/3). Attente de 20s...")
                derniere_erreur = e
                if attempt < 2:
                    time.sleep(20)

            except Exception as e:
                print(f"❌ Erreur inattendue avec {modele} : {e}")
                derniere_erreur = e
                break

        # Si on arrive ici, c'est que toutes les tentatives pour ce modèle ont échoué
        print(f"❌ Échec complet pour le modèle {modele}. Passage au modèle suivant...")

    # Si aucun modèle n'a fonctionné
    print("❌ Aucun modèle Gemini n'a pu générer le script après toutes les tentatives.")
    raise derniere_erreur