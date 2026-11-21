import os
import requests
import time
import urllib.parse

def chercher_visuels(mots_cles):
    """Génère des images verticales via Pollinations.ai."""
    chemins_images = []
    os.makedirs("output/visuels", exist_ok=True)

    # On s'assure d'avoir au moins 4 mots-clés solides
    while len(mots_cles) < 4:
        mots_cles.append("Africa mystery cinematic dark")

    print(f"📝 Mots-clés reçus : {mots_cles[:4]}")

    for i, mot in enumerate(mots_cles[:4]): # On se limite à 4 images
        prompt = f"{mot}, style sombre, mystérieux, éclairage cinématographique, haute qualité"
        prompt_encode = urllib.parse.quote(prompt)
        # Format 1080x1920 (portrait) pour YouTube Shorts
        url_image = f"https://image.pollinations.ai/prompt/{prompt_encode}?width=1080&height=1920&nologo=true&seed={i}"

        succes = False
        for tentative in range(2):
            try:
                print(f"🎨 Génération de l'image {i+1}/4 (Tentative {tentative+1}) : '{mot}'...")
                response = requests.get(url_image, timeout=60)
                
                if response.status_code == 200:
                    chemin_image = f"output/visuels/img_generee_{i}.jpg"
                    with open(chemin_image, 'wb') as f:
                        f.write(response.content)
                    chemins_images.append(chemin_image)
                    print(f"✅ Image sauvegardée : {chemin_image}")
                    succes = True
                    break
                else:
                    print(f"⚠️ Échec HTTP {response.status_code}")
            except Exception as e:
                print(f"❌ Erreur réseau : {e}")
            
            time.sleep(3)

        if not succes:
            print(f"❌ Impossible de générer l'image pour '{mot}'")

        time.sleep(2)

    return chemins_images