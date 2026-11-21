import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def uploader_video(chemin_video, titre, description, tags):
    """Upload une vidéo sur YouTube en utilisant les secrets GitHub."""
    
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        print("❌ ERREUR : Les identifiants YouTube ne sont pas tous définis dans les secrets.")
        return None

    # Création des identifiants avec le Refresh Token
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    # Construction du client YouTube
    youtube = build("youtube", "v3", credentials=creds)

    # Préparation des métadonnées
    body = {
        "snippet": {
            "title": titre[:100], # Limite YouTube
            "description": description[:5000], # Limite YouTube
            "tags": tags,
            "categoryId": "24" # 24 = Entertainment
        },
        "status": {
            "privacyStatus": "public", # "private" pour tester sans publier
            "selfDeclaredMadeForKids": False
        }
    }

    # Upload avec reprise en cas de coupure
    media = MediaFileUpload(chemin_video, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    print("📤 Upload de la vidéo sur YouTube en cours...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   Progression : {int(status.progress() * 100)}%")

    print(f"✅ Vidéo publiée avec succès ! ID YouTube : {response['id']}")
    return response["id"]