import os
import json
from openai import OpenAI

def generer_script_docu():
    """Génère le script du documentaire via Groq (API compatible OpenAI)."""
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get("GROQ_API_KEY")
    )

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

    print("🤖 Génération du script long via Groq (openai/gpt-oss-120b)...")
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=8192
    )

    raw_text = response.choices[0].message.content.strip()

    # Nettoyage de sécurité si le modèle ajoute des backticks
    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]
    raw_text = raw_text.strip()

    return json.loads(raw_text)