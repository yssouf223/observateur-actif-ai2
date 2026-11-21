import os
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, TextClip
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut

# Format vertical strict pour YouTube Shorts
LARGEUR = 1080
HAUTEUR = 1920

def assembler_video(chemins_images, chemin_audio, chemin_sortie="output/short_final.mp4", titre="Observateur Actif"):
    if not chemins_images:
        raise ValueError("Aucune image fournie.")

    os.makedirs("output", exist_ok=True)
    audio = AudioFileClip(chemin_audio)
    duree_totale = audio.duration
    
    # Durée par image avec chevauchement pour les transitions
    duree_par_image = (duree_totale / len(chemins_images)) + 0.5 
    
    clips = []
    for i, chemin_image in enumerate(chemins_images):
        # 1. Image redimensionnée pour la hauteur
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        clip = clip.resized(height=HAUTEUR) 
        
        # 2. Effet de zoom lent (Ken Burns)
        clip = clip.resized(lambda t: 1 + 0.02 * t) 
        clip = clip.with_position(("center", "center"))
        
        # 3. Transitions (Fondu)
        clip = clip.with_effects([CrossFadeIn(0.5), CrossFadeOut(0.5)])
        clips.append(clip)

    # 4. Assemblage avec chevauchement (padding négatif)
    video_finale = concatenate_videoclips(clips, method="compose", padding=-0.5)

    # 5. Fond noir au format 9:16
    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0)).with_duration(duree_totale)
    
    # 6. Superposition sur le fond
    video_composite = CompositeVideoClip([fond_noir, video_finale], size=(LARGEUR, HAUTEUR))

    # 7. Ajout du texte (Titre) en haut de la vidéo
    try:
        police = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        texte_titre = TextClip(
            text=titre,
            font=police,
            font_size=75,
            color='white',
            stroke_color='black',
            stroke_width=4,
            size=(LARGEUR - 100, None), 
            method='caption' 
        ).with_duration(4.0).with_position(('center', 'center')).with_effects([CrossFadeIn(0.5), CrossFadeOut(0.5)])
        
        video_composite = CompositeVideoClip([video_composite, texte_titre], size=(LARGEUR, HAUTEUR))
        print("✨ Titre ajouté à la vidéo.")
    except Exception as e:
        print(f"⚠️ Impossible d'ajouter le texte : {e}")

    # 8. Ajout de l'audio et écriture finale
    video_composite = video_composite.with_audio(audio)
    video_composite.write_videofile(
        chemin_sortie,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast"
    )
    print(f"🎉 Vidéo sauvegardée : {chemin_sortie}")
    return chemin_sortie