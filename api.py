
import asyncio
import websockets

from urllib.parse import urlparse, parse_qs
from handle_error import IsId
import datetime
import json
import hupper

from queue_manager import consumer_handler, producer_handler
from controller.controller import controller_e
clients = {}  # Dictionnaire pour stocker les connexions client
queue = asyncio.Queue()  # Initialisation de la queue pour stocker les messages


async def handle_message(websocket, path):
    


    # Analyser l'URL et les paramètres de requête
    url = urlparse(path)
    query_params = parse_qs(url.query)
    client_id = query_params.get('id', [None])[0]

    auth_id =await IsId(websocket,client_id)
    if auth_id == False:
         del clients[client_id]

    print("success authentification id")

    clients[client_id] = websocket

    # # ajouter les fonctions de traitements des messages ici
    try:
            async for message in websocket:
                # print(f"Message ---->: {message}")
                # if message == "fermer":
                #     await websocket.send("Fermeture de la connexion sur demande du client.")
                #     await websocket.close()
                #     break
                # else:
                print("queue : ", queue.qsize())
                await websocket.send(f"Message reçu : {message}")
                await producer_handler(message, queue)
    except websockets.exceptions.ConnectionClosed as e:
            print(e)
            print("La connexion a été fermée par le client.")
    
  



   

print("ok")
async def launch():

    # Créer une tâche pour executer le controller qui à des threads non compatible avec asyncio
    loop = asyncio.get_running_loop()
    asyncio.create_task(consumer_handler(queue, clients))
    print("Démarrage du module de queue")
  

    await loop.run_in_executor(None, controller_e, queue)
    print("Démarrage du conotroller")
    
    async with websockets.serve(handle_message, "localhost", 8765):
        print("Serveur démarré à ws://localhost:8765")
        await asyncio.Future()  # Exécute le serveur indéfiniment

def main():
    # Initialiser le reloader
# reloader = hupper.start_reloader('queu_manager.main')
    reloader = hupper.start_reloader('api.main')

    asyncio.run(launch())

if __name__ == "__main__":
    main()
