import os
import requests
import time
import base64
import concurrent.futures

CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_MODEL = "@cf/black-forest-labs/flux-1-schnell"

def _generer_image_cloudflare(prompt, i):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL}"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}
    # Format 16:9 forcé (1920x1080)
    payload = {
        "prompt": f"{prompt}, cinematic documentary style, highly detailed, 16:9",
        "steps": 4
    }
    
    for attempt in range(2): # 2 tentatives max par image
        try:
            print(f"🎨 Génération Cloudflare pour l'image {i+1}/60...")
            response = requests.post(url, headers=headers, json=payload, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data and "image" in data["result"]:
                    return base64.b64decode(data["result"]["image"])
            elif response.status_code == 429:
                print(f"⏳ Limite Cloudflare atteinte (Image {i+1}). Pause de 10s...")
                time.sleep(10)
        except Exception as e:
            print(f"❌ Erreur réseau pour l'image {i+1}: {e}")
            time.sleep(5)
            
    # 🛡️ Image de secours si Cloudflare échoue
    print(f"🔄 Basculement sur l'image de secours pour la {i+1}...")
    try:
        r = requests.get(f"https://picsum.photos/1920/1080?random={i}", timeout=20)
        if r.status_code == 200:
            return r.content
    except:
        pass
    return None

def chercher_visuels_docu(mots_cles):
    os.makedirs("output/visuels_docu", exist_ok=True)
    
    # ✅ On passe à 60 images comme demandé
    total_images = 60 
    
    base = list(mots_cles) if mots_cles else ["Africa documentary"]
    while len(base) < total_images:
        base.extend(mots_cles)
    
    chemins = []
    
    def process(i):
        contenu = _generer_image_cloudflare(base[i], i)
        if contenu:
            chemin = f"output/visuels_docu/img_{i}.jpg"
            with open(chemin, 'wb') as f:
                f.write(contenu)
            print(f"✅ Image {i+1}/60 sauvegardée.")
            return chemin
        return None

    # 2 workers en parallèle pour la rapidité, avec une petite pause
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for res in ex.map(process, range(total_images)):
            if res: chemins.append(res)
            time.sleep(1.5) 
            
    print(f"🖼️ Total : {len(chemins)} images sur {total_images}.")
    return chemins