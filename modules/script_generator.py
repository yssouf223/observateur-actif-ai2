import google.generativeai as genai
import json

def generer_script(sujet):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash') # Modèle gratuit
    
    prompt = f"""Tu es un scénariste pour une chaîne YouTube de mystères africains.
    Écris un script de 60 secondes sur le sujet : {sujet}.
    Format de sortie JSON strict :
    {{"titre": "...", "script": "...", "mots_cles_visuels": ["mot1", "mot2", ...]}}
    Le script doit être captivant, avec une accroche forte et une chute.
    """
    response = model.generate_content(prompt)
    return json.loads(response.text)
