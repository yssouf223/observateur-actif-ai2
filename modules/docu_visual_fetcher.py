import os
import requests
import time
import concurrent.futures

HF_TOKEN = os.environ.get("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

def _generer_image_hf(prompt, i):
    """Génère une image 16:9 via Hugging Face (FLUX.1-schnell)."""
    if not HF_TOKEN:
        print("❌ ERREUR : Le token HF_TOKEN n'est pas défini.")
        return None

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    # On force les dimensions pour le format 16:9 (1920x1080)
    payload = {
        "inputs": f"{prompt}, cinematic documentary style, highly detailed, 16:9",
        "parameters": {"width": 1920, "height": 1080}
    }

    for attempt in range(3):
        try:
            print(f"🎨 Génération de l'image {i+1}/60 via Hugging Face...")
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)

            if response.status_code == 200:
                return response.content  # L'image est renvoyée en bytes
            elif response.status_code == 503:
                print(f"⏳ Modèle en cours de chargement (Image {i+1}). Attente de 30s...")
                time.sleep(30)
            else:
                print(f"⚠️ Échec HTTP {response.status_code} pour l'image {i+1}.")
                time.sleep(5)
        except Exception as e:
            print(f"❌ Erreur réseau pour l'image {i+1}: {e}")
            time.sleep(10)
    return None

def chercher_visuels_docu(mots_cles):
    os.makedirs("output/visuels_docu", exist_ok=True)
    total_images = 60  # Réduit à 60 images comme demandé

    base = list(mots_cles) if mots_cles else ["Africa documentary"]
    while len(base) < total_images:
        base.extend(mots_cles)

    chemins = []

    def process(i):
        contenu = _generer_image_hf(base[i], i)
        if contenu:
            chemin = f"output/visuels_docu/img_{i}.jpg"
            with open(chemin, 'wb') as f:
                f.write(contenu)
            print(f"✅ Image {i+1}/60 sauvegardée.")
            return chemin
        return None

    # On utilise 2 workers pour ne pas surcharger l'API, avec une pause entre chaque
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for res in ex.map(process, range(total_images)):
            if res: chemins.append(res)
            time.sleep(2)  # Petite pause pour respecter les limites

    print(f"🖼️ Total : {len(chemins)} images sur {total_images}.")
    return chemins