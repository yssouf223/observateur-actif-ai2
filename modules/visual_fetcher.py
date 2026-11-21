import os
import requests
import time
import base64
import concurrent.futures

# Configuration Cloudflare Workers AI
CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_MODEL = "@cf/black-forest-labs/flux-1-schnell"

def _generer_image_cloudflare(prompt, i):
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        print("❌ ERREUR : Les identifiants Cloudflare ne sont pas définis.")
        return None

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL}"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}
    
    # L'API Cloudflare pour FLUX.1-schnell utilise "prompt" et "steps"
    payload = {
        "prompt": prompt,
        "steps": 4
    }

    try:
        print(f"🎨 Génération via Cloudflare AI pour : '{prompt[:50]}...'")
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and "result" in data and "image" in data["result"]:
                image_b64 = data["result"]["image"]
                return base64.b64decode(image_b64)
            else:
                print(f"⚠️ Réponse inattendue : {data}")
        else:
            print(f"⚠️ Échec HTTP {response.status_code} : {response.text[:200]}")
    except Exception as e:
        print(f"❌ Erreur réseau Cloudflare : {e}")
    return None

def _generer_image_secours(i):
    try:
        url = f"https://picsum.photos/1080/1920?random={i}"
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            return r.content
    except Exception:
        pass
    return None

def _generer_une(args):
    mot, i, chemin = args
    prompt = f"{mot}, style sombre, mystérieux, éclairage cinématographique, haute qualité"

    contenu = _generer_image_cloudflare(prompt, i)
    if contenu:
        with open(chemin, 'wb') as f:
            f.write(contenu)
        print(f"✅ Image {i+1} générée via Cloudflare AI.")
        return chemin

    print(f"🔄 Basculement sur l'image de secours pour le slot {i+1}...")
    contenu = _generer_image_secours(i)
    if contenu:
        with open(chemin, 'wb') as f:
            f.write(contenu)
        print(f"✅ Image de secours {i+1} sauvegardée.")
        return chemin

    return None

def chercher_visuels(mots_cles):
    os.makedirs("output/visuels", exist_ok=True)
    total_images = 6 
    
    # On s'assure d'avoir 6 mots-clés
    base = list(mots_cles) if mots_cles else ["Africa mystery"]
    mots_etendus = []
    while len(mots_etendus) < total_images:
        mots_etendus.extend(base)
    mots_etendus = mots_etendus[:total_images]

    tasks = [(mots_etendus[i], i, f"output/visuels/img_generee_{i}.jpg") for i in range(total_images)]

    chemins = []
    print(f"🎨 Génération de {total_images} images via Cloudflare AI...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for result in ex.map(_generer_une, tasks):
            if result:
                chemins.append(result)
            time.sleep(2)

    print(f"🖼️ Total : {len(chemins)} images récupérées.")
    return chemins