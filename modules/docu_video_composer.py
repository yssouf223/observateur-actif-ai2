import os
import random
import glob
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, TextClip, CompositeAudioClip, afx
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut

LARGEUR = 1920
HAUTEUR = 1080
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def assembler_video_docu(chemins_images, chemin_audio, chemin_sortie, titre):
    voix_audio = AudioFileClip(chemin_audio)
    duree_totale = voix_audio.duration
    n = len(chemins_images)
    overlap = 1.0
    
    duree_par_image = (duree_totale + (n - 1) * overlap) / n
    print(f"⏱️ Durée : {duree_totale/60:.1f} minutes | {n} images | {duree_par_image:.1f}s/image")

    clips = []
    for chemin_image in chemins_images:
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        clip = clip.resized(height=HAUTEUR)
        
        clip = clip.resized(lambda t: 1 + 0.05 * (t / duree_par_image))
        clip = clip.with_position(("center", "center"))
        
        clip = clip.with_effects([CrossFadeIn(overlap), CrossFadeOut(overlap)])
        clips.append(clip)

    video_finale = concatenate_videoclips(clips, method="compose", padding=-overlap)
    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0)).with_duration(duree_totale)
    video_composite = CompositeVideoClip([fond_noir, video_finale], size=(LARGEUR, HAUTEUR))

    try:
        titre_clip = TextClip(
            text=titre, font=POLICE, font_size=80, color='white',
            stroke_color='black', stroke_width=4,
            size=(LARGEUR - 200, None), method='caption'
        ).with_duration(5).with_position(('center', 'center')).with_effects([CrossFadeIn(0.5), CrossFadeOut(0.5)])
        video_composite = CompositeVideoClip([video_composite, titre_clip], size=(LARGEUR, HAUTEUR))
    except Exception as e:
        print(f"⚠️ Titre non ajouté : {e}")

    musiques = glob.glob("assets/music/*.mp3")
    if musiques:
        musique = AudioFileClip(random.choice(musiques))
        if musique.duration < duree_totale:
            # ✅ LA CORRECTION EST ICI : On utilise afx.AudioLoop pour l'audio
            musique = musique.with_effects([afx.AudioLoop(duration=duree_totale)])
        else:
            musique = musique.subclipped(0, duree_totale)
            
        musique = musique.with_effects([afx.MultiplyVolume(0.10)])
        video_composite = video_composite.with_audio(CompositeAudioClip([voix_audio, musique]))
    else:
        video_composite = video_composite.with_audio(voix_audio)

    video_composite.write_videofile(
        chemin_sortie, fps=24, codec="libx264", audio_codec="aac", preset="ultrafast"
    )
    return chemin_sortie 