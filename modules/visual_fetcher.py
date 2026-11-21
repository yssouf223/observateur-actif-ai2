import os
import requests
import time
import urllib.parse

def chercher_visuels(mots_cles, nombre_par_mot=1):
    """
    Génère et télécharge des images via l'API gratuite et anonyme de Pollinations.ai.
    Prend une liste de mots-clés (en anglais) et génère une image pour chacun.
    """
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    for i, mot in enumerate(mots_cles):
        # On construit un prompt un peu plus descriptif pour guider l'IA
        prompt = f"{mot}, style sombre et mystérieux, éclairage cinématographique, haute qualité"
        prompt_encode = urllib.parse.quote(prompt)
        
        # L'URL de base de l'API Pollinations (pas de clé nécessaire)
        # On force une taille carrée (1024x1024) qui sera ensuite adaptée
        url_image = f"https://image.pollinations.ai/prompt/{prompt_encode}?width=1024&height=1024&nologo=false&seed={i}"

        try:
            print(f"🎨 Génération de l'image pour : '{mot}'...")
            response = requests.get(url_image, timeout=60) # Timeout un peu long car la génération peut prendre du temps
            
            if response.status_code == 200:
                chemin_image = f"output/visuels/img_generee_{i}.jpg"
                with open(chemin_image, 'wb') as f:
                    f.write(response.content)
                chemins_images.append(chemin_image)
                print(f"✅ Image générée et sauvegardée : {chemin_image}")
            else:
                print(f"⚠️ Échec de la génération (code {response.status_code}) pour '{mot}'")
        
        except Exception as e:
            print(f"❌ Erreur lors de la génération pour '{mot}': {e}")

        # Pause obligatoire de 15 secondes entre chaque requête pour respecter la limite
        # On ne fait la pause que s'il reste des mots-clés à traiter
        if i < len(mots_cles) - 1:
            print("⏳ Pause de 15 secondes pour respecter la limite de l'API...")
            time.sleep(15)

    return chemins_images