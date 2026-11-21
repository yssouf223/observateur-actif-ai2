import os
import re
import random
import glob
from moviepy import (
    ImageClip, AudioFileClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, TextClip, CompositeAudioClip, afx
)
from moviepy.video.fx import CrossFadeIn, CrossFadeOut

LARGEUR = 1080
HAUTEUR = 1920
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def _decouper_sous_titres(script, max_chars=35):
    script = (script or "").strip()
    phrases = re.split(r'(?<=[.!?,;:])\s+', script)
    blocs = []
    for p in phrases:
        p = p.strip()
        if not p:
            continue
        if len(p) <= max_chars:
            blocs.append(p)
        else:
            mots = p.split()
            courant = ""
            for m in mots:
                if len(courant) + len(m) + 1 <= max_chars or not courant:
                    courant = (courant + " " + m).strip()
                else:
                    blocs.append(courant)
                    courant = m
            if courant:
                blocs.append(courant)
    return blocs

def assembler_video(chemins_images, chemin_audio, chemin_sortie="output/short_final.mp4",
                    titre="Observateur Actif", script_texte=""):
    if not chemins_images:
        raise ValueError("Aucune image fournie.")

    os.makedirs("output", exist_ok=True)
    voix_audio = AudioFileClip(chemin_audio)
    duree_totale = voix_audio.duration

    n = len(chemins_images)
    overlap = 0.5 

    duree_par_image = (duree_totale + (n - 1) * overlap) / n
    print(f"⏱️ Durée audio : {duree_totale:.1f}s | {n} images | {duree_par_image:.1f}s/image")

    # 1) Clips d'image
    clips = []
    for chemin_image in chemins_images:
        clip = ImageClip(chemin_image).with_duration(duree_par_image)
        clip = clip.resized(height=HAUTEUR)
        clip = clip.with_position(("center", "center"))
        clip = clip.with_effects([CrossFadeIn(overlap), CrossFadeOut(overlap)])
        clips.append(clip)

    video_finale = concatenate_videoclips(clips, method="compose", padding=-overlap)

    fond_noir = ColorClip(size=(LARGEUR, HAUTEUR), color=(0, 0, 0)).with_duration(duree_totale)
    video_composite = CompositeVideoClip([fond_noir, video_finale], size=(LARGEUR, HAUTEUR))

    # 2) Titre
    try:
        titre_clip = TextClip(
            text=titre, font=POLICE, font_size=80, color='white',
            stroke_color='black', stroke_width=4,
            size=(LARGEUR - 100, None), method='caption'
        ).with_duration(3).with_position(('center', 'center')).with_effects([CrossFadeIn(0.4), CrossFadeOut(0.4)])
        video_composite = CompositeVideoClip([video_composite, titre_clip], size=(LARGEUR, HAUTEUR))
    except Exception as e:
        print(f"⚠️ Titre non ajouté : {e}")

    # 3) Sous-titres
    if script_texte:
        try:
            blocs = _decouper_sous_titres(script_texte, max_chars=32)
            total_chars = sum(len(b) for b in blocs) or 1
            t_courant = 0.0
            sous_titres = []
            for bloc in blocs:
                duree = (len(bloc) / total_chars) * duree_totale
                if duree < 0.4: duree = 0.4
                clip_txt = TextClip(
                    text=bloc, font=POLICE, font_size=62, color='white',
                    stroke_color='black', stroke_width=4,
                    size=(LARGEUR - 120, None), method='caption'
                ).with_duration(duree).with_start(t_courant).with_position(('center', HAUTEUR - 450))
                sous_titres.append(clip_txt)
                t_courant += duree
            video_composite = CompositeVideoClip([video_composite] + sous_titres, size=(LARGEUR, HAUTEUR))
        except Exception as e:
            print(f"⚠️ Sous-titres non ajoutés : {e}")

    # 4) 🎵 Musique de fond depuis assets/music/ 🎵
    musiques = glob.glob("assets/music/*.mp3")
    if musiques:
        musique_choisie = random.choice(musiques)
        print(f"🎶 Musique de fond sélectionnée : {musique_choisie}")
        
        musique = AudioFileClip(musique_choisie)
        if musique.duration < duree_totale:
            boucles = int(duree_totale / musique.duration) + 1
            musiques_bouclees = [musique] * boucles
            musique = concatenate_videoclips(musiques_bouclees)
            musique = musique.with_duration(duree_totale)
        else:
            musique = musique.subclipped(0, duree_totale)
            
        musique = musique.with_effects([afx.MultiplyVolume(0.15)])
        audio_final = CompositeAudioClip([voix_audio, musique])
        video_composite = video_composite.with_audio(audio_final)
        print("✨ Voix et musique mixées.")
    else:
        print("⚠️ Aucune musique trouvée dans assets/music/. La vidéo aura juste la voix.")
        video_composite = video_composite.with_audio(voix_audio)

    # 5) Export
    video_composite.write_videofile(
        chemin_sortie,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        preset="ultrafast"
    )
    print(f"🎉 Vidéo sauvegardée : {chemin_sortie}")
    return chemin_sortie