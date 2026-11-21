import os
import requests
import time
import urllib.parse

def chercher_visuels(mots_cles):
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    # On s'assure d'avoir au moins 6 mots-clés
    while len(mots_cles) < 6:
        mots_cles.append("Africa mystery dark cinematic")

    for i, mot in enumerate(mots_cles[:6]): # On limite à 6 images max
        prompt = f"{mot}, style sombre et mystérieux, éclairage cinématographique, haute qualité"
        prompt_encode = urllib.parse.quote(prompt)
        url_image = f"https://image.pollinations.ai/prompt/{prompt_encode}?width=1080&height=1920&nologo=true&seed={i}"

        try:
            print(f"🎨 Génération de l'image {i+1}/6 : '{mot}'...")
            response = requests.get(url_image, timeout=45)
            
            if response.status_code == 200:
                chemin_image = f"output/visuels/img_generee_{i}.jpg"
                with open(chemin_image, 'wb') as f:
                    f.write(response.content)
                chemins_images.append(chemin_image)
                print(f"✅ Image sauvegardée : {chemin_image}")
            else:
                print(f"⚠️ Échec pour '{mot}'")
        except Exception as e:
            print(f"❌ Erreur : {e}")

        time.sleep(2) # Petite pause

    return chemins_images