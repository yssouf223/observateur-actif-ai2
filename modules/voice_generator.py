import edge_tts
import asyncio

async def generer_voix(texte, chemin_sortie="output/voix.mp3"):
    """Génère un fichier audio à partir d'un texte avec une voix française."""
    # Voix recommandée pour un ton mystérieux : "fr-FR-DeniseNeural"
    # Alternative masculine : "fr-FR-HenriNeural"
    voix = "fr-FR-DeniseNeural"
    
    # On ajuste légèrement le débit pour un rendu plus naturel
    communicate = edge_tts.Communicate(texte, voice=voix, rate="+5%")
    await communicate.save(chemin_sortie)
    return chemin_sortie