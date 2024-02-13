
import asyncio
import websockets

from urllib.parse import urlparse, parse_qs
from handle_error import IsId
import datetime
import json
import hupper

from queue_manager import consumer_handler, producer_handler

clients = {}  # Dictionnaire pour stocker les connexions client
queue = asyncio.Queue()  # Initialisation de la queue pour stocker les messages


async def close_connection_to_specific_client(id):
    client_websocket = clients[id]
    await client_websocket.send(f"Fermeture de la connexion du client ${id}")
    await client_websocket.close()
    del clients[id]


async def server_message_event_to_specific_client(id=None):
    client_id = clients[id]
    event_data = {
            'type': 'emit',
            'time': datetime.datetime.utcnow().isoformat(),
            'phase': 'launch'
            'url' 'url',
            'xpath_sequence': ["séquence une xppath", "séquence deux xpath", "séquence trois xpath"],
            'data': 'data is comming!',
            'device_id' : id,
            'city': 'city',
            'price_limit': 'price_limit',
            'ban words' : 'ban words'
        }
        
        # Convert the event data to a JSON string to send
    event_message = json.dumps(event_data)

    # dans ce cas client_id est un websocket
    await client_id.send(event_message)



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
    except websockets.exceptions.ConnectionClosed:
            print("La connexion a été fermée par le client.")
  



   

print("ok")
async def launch():
    asyncio.create_task(consumer_handler(queue))
    print("Démarrage du module de queue")
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
