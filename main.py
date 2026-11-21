import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from modules.story_fetcher import choisir_sujet
from modules.script_generator import generer_script
from modules.voice_generator import generer_voix
from modules.visual_fetcher import chercher_visuels
from modules.music_generator import generer_musique_fond
from modules.video_composer import assembler_video

load_dotenv()

async def pipeline_creation_video():
    print(f"🚀 Démarrage du pipeline - {datetime.now()}")
    os.makedirs("output", exist_ok=True)

    # 1. Sujet
    sujet = choisir_sujet()
    print(f"📖 Sujet choisi : {sujet}")

    # 2. Script
    script_data = generer_script(sujet)
    print(f"✍️ Script généré : {script_data['titre']}")

    # 3. Voix
    chemin_audio = "output/voix.mp3"
    await generer_voix(script_data['script'], chemin_audio)
    print(f"🎙️ Voix off générée : {chemin_audio}")

    # 4. Musique (NOUVEAU)
    chemin_musique = "output/musique.mp3"
    chemin_musique = generer_musique_fond(chemin_musique, duree=50)

    # 5. Images (Cloudflare)
    chemins_visuels = chercher_visuels(script_data['mots_cles_visuels'])
    print(f"🖼️ {len(chemins_visuels)} visuels générés")

    if not chemins_visuels:
        raise Exception("❌ Aucune image générée, arrêt du pipeline.")

    # 6. Assemblage
    chemin_video = "output/short_final.mp4"
    assembler_video(
        chemins_visuels,
        chemin_audio,
        chemin_video,
        script_data['titre'],
        script_data['script'],
        chemin_musique  # On passe la musique à l'assembleur
    )
    print(f"🎬 Vidéo finale prête : {chemin_video}")

    return chemin_video, script_data

if __name__ == "__main__":
    asyncio.run(pipeline_creation_video())