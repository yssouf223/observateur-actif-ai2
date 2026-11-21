import os
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, TextClip
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut, Resize

LARGEUR = 1080
HAUTEUR = 1920

def assembler_video(chemins_images, chemin_audio, chemin_sortie="output/short_final.mp4", titre="Observateur Actif"):
    if not chemins_images:
        raise ValueError("Aucune image fournie.")

    os.makedirs("output", exist_ok=True)
    audio = AudioFileClip(chemin_audio)
    duree_totale = audio.duration
    
    # On calcule la durée par image (on ajoute 0.5s pour le chevauchement des transitions)
    duree_par_image = (duree_totale / len(chemins_images)) + 0.5 
    
    clips = []
    for i, chemin_image in enumerate(chemins_images):
        # 1. L'image avec un léger effet de zoom (Ken Burns)
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        clip = clip.resized(lambda t: 1 + 0.04 * t) # Zoom de 4% progressif
        clip = clip.with_position(("center", "center"))
        
        # 2. Transitions (Fondu au début et à la fin de chaque image)
        clip = clip.with_effects([CrossFadeIn(0.5), CrossFadeOut(0.5)])
        clips.append(clip)

    # 3. On assemble les images (le padding permet aux fondus de se chevaucher)
    video_finale = concatenate_videoclips(clips, method="compose", padding=-0.5)

    # 4. Fond noir de sécurité
    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0)).with_duration(duree_totale)
    video_composite = CompositeVideoClip([fond_noir, video_finale], size=(LARGEUR, HAUTEUR))

    # 5. Ajout du texte (Titre) par-dessus pendant les 3 premières secondes
    try:
        # On crée un clip de texte simple (on utilise la police par défaut)
        texte_titre = TextClip(
            text=titre,
            font_size=70,
            color='white',
            stroke_color='black',
            stroke_width=3,
            size=(LARGEUR - 100, None), # Largeur max de 980px
            method='caption' # Le texte passe à la ligne automatiquement
        ).with_duration(3.5).with_position(('center', 'center')).with_effects([CrossFadeIn(0.5), CrossFadeOut(0.5)])
        
        video_composite = CompositeVideoClip([video_composite, texte_titre], size=(LARGEUR, HAUTEUR))
        print("✨ Titre ajouté à la vidéo.")
    except Exception as e:
        print(f"⚠️ Impossible d'ajouter le texte (police manquante) : {e}")

    # 6. Ajout de l'audio et écriture
    video_composite = video_composite.with_audio(audio)
    video_composite.write_videofile(
        chemin_sortie,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast" # Option magique pour accélérer le rendu sur GitHub
    )
    print(f"🎉 Vidéo sauvegardée : {chemin_sortie}")
    return chemin_sortie