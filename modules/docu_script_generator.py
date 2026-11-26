import os
import json
import time
import httpx
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

MODELES = ["gemini-3.8-flash", "gemini-3.6-flash", "gemini-2.5-flash"]

def generer_script_docu():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    # On demande 2200 mots pour être sûr que ça rentre dans la limite
    prompt = """Tu es un réalisateur de documentaires pour la chaîne YouTube "Observateur Actif".
Écris un script d'environ 2200 mots sur un mystère, une histoire insolite ou une légende méconnue d'Afrique.
Structure ton récit avec une introduction captivante, 3 chapitres distincts, et une conclusion.
Le ton doit être grave, sérieux, documentaire et immersif.
Fournis la réponse UNIQUEMENT sous forme d'objet JSON :
{
    "titre": "Un titre accrocheur pour le documentaire",
    "script": "Le texte complet du script (2200 mots)",
    "mots_cles_visuels": ["une liste de 15 mots-clés en anglais pour générer des images"]
}
"""
    derniere_erreur = None
    for modele in MODELES:
        for attempt in range(3):
            try:
                print(f"🤖 Génération du script long avec {modele}...")
                response = client.models.generate_content(
                    model=modele,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        max_output_tokens=8192,  # 👈 ON AUGMENTE LA LIMITE ICI
                        temperature=0.7
                    ),
                )
                
                # Nettoyage de sécurité au cas où l'IA ajoute du texte avant/après
                raw_text = response.text.strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                
                return json.loads(raw_text)
                
            except (ServerError, httpx.RemoteProtocolError) as e:
                print(f"⚠️ Surcharge (Essai {attempt+1}). Attente 20s...")
                time.sleep(20)
            except ClientError as e:
                if "404" in str(e):
                    break
                time.sleep(20)
            except json.JSONDecodeError as e:
                print(f"⚠️ Erreur JSON avec {modele}. On réessaie...")
                time.sleep(10)
            except Exception as e:
                derniere_erreur = e
                break
    raise derniere_erreur