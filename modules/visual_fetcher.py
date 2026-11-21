import os
import asyncio
from putergenai import PuterClient
import requests
import time

# Modèle d'image. Tu peux essayer "dall-e-3" ou "flux" si tu veux.
MODELE_IMAGE = "pollinations-image"

async def _generer_une_image(client, prompt, chemin_sortie):
    """Fonction interne pour générer une seule image."""
    try:
        print(f"🎨 Génération de l'image pour : '{prompt}'...")
        image_url = await client.ai_txt2img(prompt, model=MODELE_IMAGE)
        
        response = requests.get(image_url, timeout=60)
        if response.status_code == 200:
            with open(chemin_sortie, 'wb') as f:
                f.write(response.content)
            print(f"✅ Image sauvegardée : {chemin_sortie}")
            return chemin_sortie
        else:
            print(f"⚠️ Impossible de télécharger l'image depuis {image_url}")
            return None
    except Exception as e:
        print(f"❌ Erreur lors de la génération pour '{prompt}': {e}")
        return None

async def chercher_visuels(mots_cles):
    """
    Génère des images via Puter.js en utilisant le token stocké
    dans la variable d'environnement PUTER_TOKEN.
    """
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    # Récupération du token depuis les variables d'environnement
    token = os.environ.get("PUTER_TOKEN")
    
    if not token:
        print("❌ ERREUR : Le token Puter (PUTER_TOKEN) n'est pas défini.")
        return []

    # Initialisation du client avec le token directement (pas besoin de login)
    async with PuterClient(token=token) as client:
        print("✅ Client Puter initialisé avec le token.")

        for i, mot in enumerate(mots_cles):
            prompt = f"{mot}, style sombre et mystérieux, éclairage cinématographique, haute qualité, illustration"
            chemin_image = f"output/visuels/img_generee_{i}.jpg"
            
            resultat = await _generer_une_image(client, prompt, chemin_image)
            if resultat:
                chemins_images.append(resultat)

            if i < len(mots_cles) - 1:
                time.sleep(3)  # Pause pour ne pas surcharger l'API

    return chemins_images