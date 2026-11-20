import os
import requests
from pexels import Client
import time

def chercher_visuels(mots_cles, nombre_par_mot=1):
    """Cherche et télécharge des images en orientation portrait pour chaque mot-clé."""
    # Initialisation du client Pexels
    client = Client(api_key=os.environ.get("PEXELS_API_KEY"))
    
    chemins_images = []
    
    # On s'assure que le dossier de sortie existe
    os.makedirs("output/visuels", exist_ok=True)
    
    for i, mot in enumerate(mots_cles):
        try:
            # Recherche d'images en orientation portrait
            resultats = client.search_photos(
                query=mot,
                orientation="portrait",
                size="large",
                per_page=nombre_par_mot
            )
            
            for j, photo in enumerate(resultats.get("photos", [])):
                # On récupère l'URL de l'image en haute qualité
                url_image = photo["src"]["large"]
                
                # Téléchargement de l'image
                response = requests.get(url_image, stream=True)
                if response.status_code == 200:
                    chemin_image = f"output/visuels/img_{i}_{j}.jpg"
                    with open(chemin_image, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    chemins_images.append(chemin_image)
                    print(f"✅ Image téléchargée : {chemin_image}")
                else:
                    print(f"⚠️ Impossible de télécharger l'image : {url_image}")
                
                # Petite pause pour respecter les limites de l'API
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Erreur pour le mot-clé '{mot}': {e}")
            
    return chemins_images