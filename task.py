from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import pandas as pd
from datetime import datetime
import os
import asyncio

# Variables pour la connexion
api_id = '25846172'  # Remplacez par votre API ID
api_hash = 'f476b94eae369562cd2ac993a145e6cb'  # Remplacez par votre API Hash
channel_username = 'momo'  # Remplacez par le nom d'utilisateur du canal
output_dir = 'parquet_files'  # Répertoire de sortie des fichiers Parquet

# Fonction asynchrone pour récupérer les messages
async def main():
    # Créer le client Telegram
    async with TelegramClient('nouvelle_session', api_id, api_hash) as client:
        # Assurez-vous que le répertoire existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Récupérer les messages du canal
        messages = []
        async for message in client.iter_messages(channel_username):
            if message.text:  # Ignorer les messages sans texte
                messages.append({
                    "timestamp": message.date,
                    "source": channel_username,
                    "text": message.message,
                    "has_media": isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument))
                })

        # Vérifier si des messages ont été récupérés
        if messages:
            # Convertir en DataFrame Pandas
            df = pd.DataFrame(messages)

            # Enregistrer au format Parquet
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            parquet_file = f"{output_dir}/messages_{timestamp}.parquet"
            df.to_parquet(parquet_file, engine='pyarrow')
            print(f"Fichier Parquet enregistré dans {parquet_file}")
        else:
            print("Aucun message trouvé dans le canal.")

# Vérifier si nous sommes dans un environnement interactif
try:
    # Si nous sommes dans un Jupyter Notebook, utiliser asyncio.create_task
    asyncio.create_task(main())
except RuntimeError:
    # Si nous ne sommes pas dans un environnement interactif, utiliser asyncio.run()
    asyncio.run(main())