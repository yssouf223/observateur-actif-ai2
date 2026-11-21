import os
import requests
import time
import urllib.parse

def chercher_visuels(mots_cles):
    """
    Génère et télécharge des images via l'API gratuite et anonyme de Pollinations.ai.
    Prend une liste de mots-clés (en anglais) et génère une image pour chacun.
    """
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    for i, mot in enumerate(mots_cles):
        # On construit un prompt descriptif pour guider l'IA
        prompt = f"{mot}, style sombre et mystérieux, éclairage cinématographique, haute qualité"
        prompt_encode = urllib.parse.quote(prompt)
        
        # L'URL de l'API Pollinations (pas de clé nécessaire)
        url_image = f"https://image.pollinations.ai/prompt/{prompt_encode}?width=1024&height=1024&nologo=true&seed={i}"

        try:
            print(f"🎨 Génération de l'image pour : '{mot}'...")
            response = requests.get(url_image, timeout=60)
            
            if response.status_code == 200:
                chemin_image = f"output/visuels/img_generee_{i}.jpg"
                with open(chemin_image, 'wb') as f:
                    f.write(response.content)
                chemins_images.append(chemin_image)
                print(f"✅ Image sauvegardée : {chemin_image}")
            else:
                print(f"⚠️ Échec de la génération (code {response.status_code}) pour '{mot}'")
        
        except Exception as e:
            print(f"❌ Erreur lors de la génération pour '{mot}': {e}")

        # Pause de 5 secondes entre chaque requête pour respecter les limites
        if i < len(mots_cles) - 1:
            print("⏳ Pause de 5 secondes...")
            time.sleep(5)

    return chemins_images