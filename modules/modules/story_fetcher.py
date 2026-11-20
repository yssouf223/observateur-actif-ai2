import random

# Une liste de sujets d'histoires mystérieuses et insolites d'Afrique.
# Tu peux enrichir cette liste avec tes propres recherches.
SUJETS = [
    "La cité perdue de Djenné-Djenno au Mali",
    "Les mystérieux cercles de pierres de Senegambia",
    "La légende du peuple Dogon et de Sirius B",
    "Les tombeaux étranges de l'île de Gorée",
    "Le mythe du serpent-dieu Damballa en Haïti (origine africaine)",
    "Les gravures rupestres inexpliquées du Sahara",
    "L'histoire du royaume fantôme du Kongo",
    "Les esprits de la forêt sacrée de la Casamance",
    "Le trésor caché de l'empereur du Mali, Mansa Moussa",
    "Les pratiques mystérieuses du peuple Himba en Namibie"
]

def choisir_sujet():
    """Choisit un sujet aléatoire dans la liste."""
    return random.choice(SUJETS)