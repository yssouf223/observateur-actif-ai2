import os
import requests
import time

def generer_musique_fond(chemin_sortie="output/musique.mp3", duree=50):
    """Génère une musique via Hugging Face (MusicGen)."""
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("❌ ERREUR : Le token Hugging Face (HF_TOKEN) n'est pas défini.")
        return None

    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {hf_token}"}
    
    prompt = "dark mysterious ambient cinematic soundtrack, suspenseful, african mystery, instrumental, no vocals"
    payload = {
        "inputs": prompt,
        "parameters": {"duration": duree}
    }

    max_retries = 4
    for attempt in range(max_retries):
        try:
            print(f"🎵 Génération de la musique via Hugging Face (Tentative {attempt+1}/{max_retries})...")
            response = requests.post(API_URL, headers=headers, json=payload, timeout=180)

            if response.status_code == 200:
                with open(chemin_sortie, "wb") as f:
                    f.write(response.content)
                print(f"✅ Musique de fond générée : {chemin_sortie}")
                return chemin_sortie
            elif response.status_code == 503:
                print("⏳ Le modèle musical est en cours de chargement sur Hugging Face. Attente de 30s...")
                time.sleep(30)
            else:
                print(f"⚠️ Échec HTTP {response.status_code} : {response.text[:200]}")
                break
        except Exception as e:
            print(f"❌ Erreur réseau : {e}")
            break
            
    print("❌ Impossible de générer la musique après plusieurs tentatives.")
    return None