import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from modules.story_fetcher import choisir_sujet
from modules.script_generator import generer_script
from modules.voice_generator import generer_voix
from modules.visual_fetcher import chercher_visuels
from modules.video_composer import assembler_video

# Chargement des variables d'environnement (pour le test local)
load_dotenv()

async def pipeline_creation_video():
    """Pipeline principal pour créer une vidéo Short."""
    print(f"🚀 Démarrage du pipeline - {datetime.now()}")

    # 1. Création du dossier de sortie
    os.makedirs("output", exist_ok=True)

    # 2. Choix du sujet
    sujet = choisir_sujet()
    print(f"📖 Sujet choisi : {sujet}")

    # 3. Génération du script
    script_data = generer_script(sujet)
    print(f"✍️ Script généré : {script_data['titre']}")

    # 4. Génération de la voix off (async)
    chemin_audio = "output/voix.mp3"
    await generer_voix(script_data['script'], chemin_audio)
    print(f"🎙️ Voix off générée : {chemin_audio}")

    # 5. Génération des visuels avec Pollinations
    chemins_visuels = chercher_visuels(script_data['mots_cles_visuels'])
    print(f"🖼️ {len(chemins_visuels)} visuels générés")

    if not chemins_visuels:
        raise Exception("❌ Aucune image générée, arrêt du pipeline.")

    # 6. Assemblage de la vidéo
    chemin_video = "output/short_final.mp4"
    assembler_video(chemins_visuels, chemin_audio, chemin_video, script_data['titre'])
    print(f"🎬 Vidéo finale prête : {chemin_video}")

    return chemin_video, script_data

if __name__ == "__main__":
    asyncio.run(pipeline_creation_video())