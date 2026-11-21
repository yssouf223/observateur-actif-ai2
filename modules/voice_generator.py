import edge_tts

async def generer_voix(texte, chemin_sortie="output/voix.mp3"):
    voix = "fr-FR-DeniseNeural"
    communicate = edge_tts.Communicate(texte, voice=voix, rate="+5%")
    await communicate.save(chemin_sortie)
    return chemin_sortie