from sources.gmail import get_gmail_service

if __name__ == "__main__":
    # Authentifier l'utilisateur et créer le fichier token.json
    service = get_gmail_service()
    print("Authentification réussie et token.json créé !")
import sys
import os

# Ajouter le répertoire racine du projet à sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from sources.gmail import get_gmail_service

if __name__ == "__main__":
    # Authentifier l'utilisateur et créer le fichier token.json
    service = get_gmail_service()
    print("Authentification réussie et token.json créé !")
