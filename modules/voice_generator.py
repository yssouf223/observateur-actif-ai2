import edge_tts

async def generer_voix(texte, chemin_sortie="output/voix.mp3"):
    voix = "fr-FR-DeniseNeural" # Voix féminine naturelle
    # Alternative : "fr-FR-HenriNeural" pour une voix masculine
    communicate = edge_tts.Communicate(texte, voice=voix, rate="+10%")
    await communicate.save(chemin_sortie)
