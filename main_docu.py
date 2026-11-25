import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

from modules.docu_script_generator import generer_script_docu
from modules.voice_generator import generer_voix
from modules.docu_visual_fetcher import chercher_visuels_docu
from modules.docu_video_composer import assembler_video_docu
from modules.youtube_uploader import uploader_video

load_dotenv()

async def pipeline_documentaire():
    print(f"🚀 Démarrage du DOCUMENTAIRE - {datetime.now()}")
    os.makedirs("output", exist_ok=True)

    # 1. Sujet et Script long
    script_data = generer_script_docu()
    print(f"✍️ Script Documentaire généré : {script_data['titre']}")

    # 2. Voix off
    chemin_audio = "output/voix_docu.mp3"
    await generer_voix(script_data['script'], chemin_audio)
    print(f"🎙️ Voix off générée : {chemin_audio}")

    # 3. Visuels (100 images)
    chemins_visuels = chercher_visuels_docu(script_data['mots_cles_visuels'])
    print(f"🖼️ {len(chemins_visuels)} visuels générés")

    if not chemins_visuels:
        raise Exception("❌ Aucune image générée.")

    # 4. Assemblage de la vidéo 16:9 (SANS SOUS-TITRES)
    chemin_video = "output/documentaire_final.mp4"
    assembler_video_docu(
        chemins_visuels,
        chemin_audio,
        chemin_video,
        script_data['titre']
        # On ne passe pas le script_texte ici
    )
    print(f"🎬 Documentaire prêt : {chemin_video}")

    # 5. Publication YouTube
    description = f"Documentaire : {script_data['titre']}.\n\n#ObservateurActif #Documentaire #Afrique #Mystère"
    tags = ["documentaire", "Afrique", "histoire", "mystère", "Observateur Actif"]
    
    uploader_video(
        chemin_video=chemin_video,
        titre=f"[DOCUMENTAIRE] {script_data['titre']}",
        description=description,
        tags=tags
    )

if __name__ == "__main__":
    asyncio.run(pipeline_documentaire())