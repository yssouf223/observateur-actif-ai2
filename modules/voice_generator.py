import edge_tts

async def generer_voix(texte, chemin_sortie="output/voix.mp3"):
    # Voix masculine multilingue de haute qualité
    voix = "fr-FR-RemyMultilingualNeural"
    
    # On ralentit légèrement le débit (-5%) et on baisse un peu la hauteur (-2Hz)
    # pour un rendu plus posé et sérieux.
    communicate = edge_tts.Communicate(
        texte, 
        voice=voix, 
        rate="-5%", 
        pitch="-2Hz"
    )
    
    await communicate.save(chemin_sortie)
    return chemin_sortie