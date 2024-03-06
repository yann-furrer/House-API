
import asyncio
import websockets

from urllib.parse import urlparse, parse_qs
from handle_error import IsId
#import hupper


from queue_manager import consumer_handler, producer_handler
from controller.thread_controller import periodical_thread, connected_list, device_planning



clients = {}  # Dictionnaire pour stocker les connexions client
queue_event =  asyncio.Queue() # Initialisation de la queue pour stocker les messages


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
                #print("queue : ", queue_event.qsize())
                await websocket.send(f"Message reçu : {message}")
                await producer_handler(message, queue_event)
    except websockets.exceptions.ConnectionClosed as e:
            print(e)
            print("La connexion a été fermée par le client.")
    
  



   


async def launch():

    # Créer une tâche pour executer le controller qui à des threads non compatible avec asyncio
    
  
    serveur_ws = await websockets.serve(handle_message, "localhost", 8765)
    
    consummer = asyncio.create_task(consumer_handler(queue_event, clients))
    device_listener = asyncio.create_task(periodical_thread(connected_list, device_planning, queue_event))

    print("Démarrage du module de queue")
    await asyncio.gather(consummer, device_listener)
    print("Serveur démarré à ws://localhost:8765\n")
    await serveur_ws.wait_closed()





# le reoader ne fonctionne pas avec asyncio.run et casse les threads
#reloader = hupper.start_reloader('api.main')

asyncio.run(launch())
