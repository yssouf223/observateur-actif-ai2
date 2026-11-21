import random

# Liste de sujets d'histoires mystérieuses et insolites d'Afrique.
# Tu peux enrichir cette liste avec tes propres trouvailles.
SUJETS = [
    "La cité perdue de Djenné-Djenno au Mali",
    "Les mystérieux cercles de pierres de Senegambia",
    "La légende du peuple Dogon et de Sirius B",
    "Les tombeaux étranges de l'île de Gorée",
    "Le mythe du serpent-dieu Damballa et ses origines africaines",
    "Les gravures rupestres inexpliquées du Sahara",
    "L'histoire du royaume fantôme du Kongo",
    "Les esprits de la forêt sacrée de la Casamance",
    "Le trésor caché de l'empereur Mansa Moussa du Mali",
    "Les pratiques mystérieuses du peuple Himba en Namibie",
    "La malédiction de la reine de Saba",
    "Les masques sacrés du peuple Yoruba",
    "Le mystère des églises taillées dans la roche de Lalibela en Éthiopie",
    "La légende du crocodile sacré de Sabou au Burkina Faso",
    "Les chants hypnotiques des pêcheurs du fleuve Niger"
]

def choisir_sujet():
    """Choisit un sujet aléatoire dans la liste."""
    return random.choice(SUJETS)