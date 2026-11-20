from pexels import Client

def chercher_visuels(mots_cles, nombre=5):
    client = Client(api_key=os.environ["PEXELS_API_KEY"])
    visuels = []
    for mot in mots_cles:
        # On force l'orientation portrait pour le format 9:16
        resultats = client.search_photos(query=mot, orientation="portrait", per_page=1)
        if resultats["photos"]:
            visuels.append(resultats["photos"][0]["src"]["large"])
    return visuels
