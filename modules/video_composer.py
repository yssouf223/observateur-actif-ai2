import os
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    ColorClip,
    concatenate_videoclips
)

# Dimensions pour un Short YouTube (9:16)
LARGEUR = 1080
HAUTEUR = 1920

def assembler_video(chemins_images, chemin_audio, chemin_sortie="output/short_final.mp4", titre="Observateur Actif"):
    """Assemble les images et l'audio en une vidéo verticale."""
    if not chemins_images:
        raise ValueError("Aucune image fournie pour l'assemblage.")

    # 1. Chargement de l'audio pour connaître sa durée
    audio = AudioFileClip(chemin_audio)
    duree_totale = audio.duration
    duree_par_image = duree_totale / len(chemins_images)
    
    clips = []
    for chemin_image in chemins_images:
        # On crée un clip à partir de chaque image
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        # On le redimensionne pour qu'il remplisse l'écran en gardant le ratio
        # (ici, on le redimensionne pour couvrir toute la hauteur)
        clip = clip.resized(height=HAUTEUR)
        # On le centre horizontalement
        clip = clip.with_position(("center", "center"))
        clips.append(clip)
    
    # 2. Concaténation des clips
    video_finale = concatenate_videoclips(clips, method="compose")
    
    # 3. Ajout de l'audio
    video_finale = video_finale.with_audio(audio)
    
    # 4. (Optionnel) Ajout d'un fond noir si l'image ne remplit pas toute la largeur
    # pour éviter les bords vides.
    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0), duration=duree_totale)
    video_finale = CompositeVideoClip([fond_noir, video_finale])
    
    # 5. Écriture du fichier final
    video_finale.write_videofile(
        chemin_sortie,
        fps=24,  # Images par seconde
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="output/temp-audio.m4a",
        remove_temp=True
    )
    
    print(f"🎉 Vidéo sauvegardée : {chemin_sortie}")
    return chemin_sortie