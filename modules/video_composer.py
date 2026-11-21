import os
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    ColorClip,
    concatenate_videoclips,
)

# Dimensions pour un Short YouTube (format 9:16 vertical)
LARGEUR = 1080
HAUTEUR = 1920

def assembler_video(chemins_images, chemin_audio, chemin_sortie="output/short_final.mp4", titre="Observateur Actif"):
    """
    Assemble les images et la voix off en une vidéo verticale au format Short.
    """
    if not chemins_images:
        raise ValueError("Aucune image fournie pour l'assemblage.")

    os.makedirs("output", exist_ok=True)

    # 1. Chargement de l'audio pour calculer la durée par image
    audio = AudioFileClip(chemin_audio)
    duree_totale = audio.duration
    duree_par_image = duree_totale / len(chemins_images)
    print(f"⏱️ Durée totale : {duree_totale:.1f}s | {duree_par_image:.1f}s par image")

    # 2. Création d'un clip pour chaque image
    clips = []
    for chemin_image in chemins_images:
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        # On redimensionne pour que l'image couvre toute la hauteur
        clip = clip.resized(height=HAUTEUR)
        # On centre l'image horizontalement
        clip = clip.with_position(("center", "center"))
        clips.append(clip)

    # 3. Concaténation des clips
    video_finale = concatenate_videoclips(clips, method="compose")

    # 4. Fond noir pour éviter les bords vides si l'image est moins large
    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0)).with_duration(duree_totale)
    video_avec_fond = CompositeVideoClip([fond_noir, video_finale], size=(LARGEUR, HAUTEUR))

    # 5. Ajout de la piste audio
    video_avec_fond = video_avec_fond.with_audio(audio)

    # 6. Écriture du fichier final
    print("🎬 Assemblage de la vidéo en cours...")
    video_avec_fond.write_videofile(
        chemin_sortie,
        fps=24,
        codec="libx264",
        audio_codec="aac",
    )

    print(f"🎉 Vidéo sauvegardée : {chemin_sortie}")
    return chemin_sortie