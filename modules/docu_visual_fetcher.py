import os
import requests
import time
import urllib.parse
import concurrent.futures

def _generer_image_pollinations(prompt, i):
    prompt_encode = urllib.parse.quote(f"{prompt}, cinematic documentary style, 16:9")
    url = f"https://image.pollinations.ai/prompt/{prompt_encode}?width=1920&height=1080&nologo=true&seed={i}"
    
    try:
        print(f"🎨 Génération via Pollinations pour la {i+1}...")
        response = requests.get(url, timeout=90)
        if response.status_code == 200:
            return response.content
        else:
            print(f"⚠️ Échec HTTP {response.status_code} pour la {i+1}")
    except Exception as e:
        print(f"❌ Erreur réseau {i}: {e}")
    return None

def chercher_visuels_docu(mots_cles):
    os.makedirs("output/visuels_docu", exist_ok=True)
    total_images = 100
    
    base = list(mots_cles) if mots_cles else ["Africa documentary"]
    while len(base) < total_images:
        base.extend(mots_cles)
    
    chemins = []
    
    def process(i):
        contenu = _generer_image_pollinations(base[i], i)
        if contenu:
            chemin = f"output/visuels_docu/img_{i}.jpg"
            with open(chemin, 'wb') as f:
                f.write(contenu)
            print(f"✅ Image {i+1}/100 sauvegardée.")
            return chemin
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        for res in ex.map(process, range(total_images)):
            if res: chemins.append(res)
            time.sleep(5)  # Pause de 5s pour respecter la limite de Pollinations
            
    return chemins