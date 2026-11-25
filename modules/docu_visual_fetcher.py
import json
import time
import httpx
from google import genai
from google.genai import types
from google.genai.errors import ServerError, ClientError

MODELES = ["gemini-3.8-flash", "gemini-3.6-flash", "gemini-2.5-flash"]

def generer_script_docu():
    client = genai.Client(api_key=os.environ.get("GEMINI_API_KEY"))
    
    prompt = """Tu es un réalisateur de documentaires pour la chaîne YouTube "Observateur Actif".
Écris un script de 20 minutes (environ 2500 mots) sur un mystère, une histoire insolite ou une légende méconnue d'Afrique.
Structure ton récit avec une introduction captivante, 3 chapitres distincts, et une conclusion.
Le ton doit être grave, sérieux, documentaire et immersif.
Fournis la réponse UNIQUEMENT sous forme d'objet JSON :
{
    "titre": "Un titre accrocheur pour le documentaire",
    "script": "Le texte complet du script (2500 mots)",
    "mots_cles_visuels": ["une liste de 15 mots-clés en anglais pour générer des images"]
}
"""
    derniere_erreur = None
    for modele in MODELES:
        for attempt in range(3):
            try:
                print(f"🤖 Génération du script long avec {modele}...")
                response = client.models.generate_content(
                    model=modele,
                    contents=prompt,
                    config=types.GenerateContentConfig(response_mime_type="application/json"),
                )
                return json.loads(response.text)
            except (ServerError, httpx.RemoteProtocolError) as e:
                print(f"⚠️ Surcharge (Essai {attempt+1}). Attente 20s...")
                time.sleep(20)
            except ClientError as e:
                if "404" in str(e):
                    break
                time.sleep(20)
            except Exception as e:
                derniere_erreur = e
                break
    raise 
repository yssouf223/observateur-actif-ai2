import os
import requests
import time
import base64
import concurrent.futures

CF_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CF_API_TOKEN = os.environ.get("CF_API_TOKEN")
CF_MODEL = "@cf/black-forest-labs/flux-1-schnell"

def _generer_image(prompt, i):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{CF_MODEL}"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}
    payload = {"prompt": f"{prompt}, cinematic documentary style, highly detailed, 16:9", "steps": 4}
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=90)
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and "result" in data:
                    return base64.b64decode(data["result"]["image"])
            elif response.status_code == 429:
                print(f"⏳ Limite API atteinte (Image {i}). Attente de 10s...")
                time.sleep(10)
        except Exception as e:
            print(f"❌ Erreur image {i}: {e}")
            time.sleep(5)
    return None

def chercher_visuels_docu(mots_cles):
    os.makedirs("output/visuels_docu", exist_ok=True)
    total_images = 100
    
    base = list(mots_cles) if mots_cles else ["Africa documentary"]
    while len(base) < total_images:
        base.extend(mots_cles)
    
    chemins = []
    
    def process(i):
        contenu = _generer_image(base[i], i)
        if contenu:
            chemin = f"output/visuels_docu/img_{i}.jpg"
            with open(chemin, 'wb') as f:
                f.write(contenu)
            print(f"✅ Image {i+1}/100 générée.")
            return chemin
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for res in ex.map(process, range(total_images)):
            if res: chemins.append(res)
            time.sleep(1)
            
    return chemins