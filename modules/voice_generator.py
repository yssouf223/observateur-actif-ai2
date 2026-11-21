import edge_tts

async def generer_voix(texte, chemin_sortie="output/voix.mp3"):
    """
    Génère un fichier audio à partir d'un texte avec une voix française.
    Utilise edge-tts : gratuit, sans clé API, voix naturelles.
    """
    # Voix féminine naturelle en français
    # Alternatives : "fr-FR-HenriNeural" (masculin), "fr-CA-SylvieNeural" (québécois)
    voix = "fr-FR-DeniseNeural"

    # Le rate="+5%" accélère légèrement le débit pour un rendu plus dynamique
    communicate = edge_tts.Communicate(texte, voice=voix, rate="+5%")
    await communicate.save(chemin_sortie)
    return chemin_sortie