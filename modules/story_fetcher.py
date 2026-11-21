import random

SUJETS = [
    "La cité perdue de Djenné-Djenno au Mali",
    "Les mystérieux cercles de pierres de Sénégambie",
    "La légende du peuple Dogon et de Sirius B",
    "Les tombeaux étranges de l'île de Gorée au Sénégal",
    "Le mystère du serpent-dieu Damballa et ses origines africaines",
    "Les gravures rupestres inexpliquées du Sahara",
    "L'histoire mystérieuse de l'ancien royaume du Kongo",
    "Les esprits et les forêts sacrées de Casamance au Sénégal",
    "Le mystère de l'expédition disparue d'Aboubakari II, empereur du Mali",
    "Les pratiques mystérieuses du peuple Himba en Namibie",
    "La reine de Saba : entre histoire, légende et mystère",
    "Les masques sacrés et les cérémonies secrètes du peuple Yoruba",
    "Le mystère des églises taillées dans la roche de Lalibela en Éthiopie",
    "Le crocodile sacré de Sabou au Burkina Faso",
    "Les chants mystérieux des pêcheurs du fleuve Niger",
    "Les mystérieuses sépultures du peuple Tellem dans les falaises de Bandiagara au Mali",
    "Le peuple oublié de Gobero et ses mystérieux cimetières dans le désert du Niger",
    "La cité abandonnée de Gedi et ses ruines mystérieuses au Kenya",
    "Les obélisques géants de l'ancienne civilisation d'Aksoum en Éthiopie",
    "Les pyramides mystérieuses du royaume de Méroé au Soudan",
    "La mystérieuse cité médiévale de Kilwa Kisiwani en Tanzanie",
    "Les peintures rupestres énigmatiques du massif de l'Ennedi au Tchad",
    "Les mystérieuses tombes monumentales de Lothagam North au Kenya",
    "Le mystère des gigantesques ruines de pierre du Grand Zimbabwe",
    "Le mystérieux rhinocéros d'or du royaume oublié de Mapungubwe en Afrique du Sud",
    "Les mystérieuses sculptures humaines de la civilisation Nok au Nigeria",
    "L'ancien observatoire astronomique de Nabta Playa dans le désert égyptien",
    "Les mystérieuses cités fortifiées de Dhar Tichitt en Mauritanie",
    "Les pyramides oubliées de l'ancienne Nubie au Soudan",
    "Les mystérieuses murailles géantes de l'ancien royaume du Bénin au Nigeria",
    "Le mystère des trésors de bronze de l'ancienne civilisation d'Igbo-Ukwu au Nigeria"
]

def choisir_sujet():
    return random.choice(SUJETS)