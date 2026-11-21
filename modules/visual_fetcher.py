import os
import asyncio
from putergenai import PuterClient
import time

# On utilise le modèle "pollinations-image" qui est fiable et gratuit.
# Tu peux essayer d'autres modèles comme "dall-e-3" ou "flux" si tu le souhaites.
MODELE_IMAGE = "pollinations-image" 

async def _generer_une_image(client, prompt, chemin_sortie):
    """Fonction interne pour générer une seule image."""
    try:
        print(f"🎨 Génération de l'image pour : '{prompt}'...")
        # L'appel à l'API de Puter
        image_url = await client.ai_txt2img(prompt, model=MODELE_IMAGE)
        
        # On télécharge l'image à partir de l'URL retournée
        import requests
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
    Génère des images via Puter.js en utilisant les identifiants stockés
    dans les variables d'environnement PUTER_USERNAME et PUTER_PASSWORD.
    """
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    # Récupération des identifiants depuis les variables d'environnement
    username = os.environ.get("PUTER_USERNAME")
    password = os.environ.get("PUTER_PASSWORD")
    
    if not username or not password:
        print("❌ ERREUR : Les identifiants Puter (PUTER_USERNAME, PUTER_PASSWORD) ne sont pas définis.")
        return []

    # Initialisation et connexion au client Puter
    async with PuterClient() as client:
        try:
            print("🔑 Connexion à Puter...")
            await client.login(username, password)
            print("✅ Connexion réussie.")
        except Exception as e:
            print(f"❌ Échec de la connexion à Puter : {e}")
            return []

        # Boucle sur chaque mot-clé pour générer une image
        for i, mot in enumerate(mots_cles):
            # On enrichit le prompt pour un style visuel cohérent avec ta chaîne
            prompt = f"{mot}, style sombre et mystérieux, éclairage cinématographique, haute qualité, illustration"
            
            chemin_image = f"output/visuels/img_generee_{i}.jpg"
            resultat = await _generer_une_image(client, prompt, chemin_image)
            
            if resultat:
                chemins_images.append(resultat)

            # Petite pause pour ne pas surcharger l'API (même si le "User-Pays" gère ça)
            if i < len(mots_cles) - 1:
                time.sleep(3) # Pause de 3 secondes

    return chemins_images