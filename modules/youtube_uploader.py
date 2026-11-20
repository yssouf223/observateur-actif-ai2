import os
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_video(file_path, title, description, tags):
    """Upload une vidéo sur YouTube en utilisant les identifiants stockés."""
    # Chargement des identifiants (le refresh token est stocké dans le fichier)
    # En production, le fichier pickle est généré après la première autorisation manuelle.
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            raise Exception("Authentification YouTube requise. Exécutez le script d'autorisation initial.")
    
    # Construction du client YouTube
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Préparation des métadonnées de la vidéo
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '24'  # 24 = Entertainment, à ajuster selon la catégorie
        },
        'status': {
            'privacyStatus': 'public',  # 'private', 'public', 'unlisted'
            'selfDeclaredMadeForKids': False
        }
    }
    
    # Upload de la vidéo
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploadé {int(status.progress() * 100)}%")
    
    print(f"✅ Vidéo uploadée avec succès ! ID: {response['id']}")
    return response['id']

# Exemple d'utilisation (à adapter dans main.py)
# if __name__ == "__main__":
#     upload_video(
#         "output/short_final.mp4",
#         "Titre de la vidéo",
#         "Description générée par l'IA",
#         ["mystère", "afrique", "insolite"]
#     )