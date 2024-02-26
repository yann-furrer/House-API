# Description: Ce fichier contient les fonctions qui permettent de gérer la queue
from controller.controller import controller
import asyncio
import json
import time
import sys
import os



# Ajouter le chemin du dossier bdd
chemin_bdd = os.path.join(os.path.dirname(__file__), 'bdd')
if chemin_bdd not in sys.path:
    sys.path.append(chemin_bdd)

# Importation des fonctions d'écriture et de lecture de la base de données
from bdd_connector import conn, cur
from bdd_read_resquest import BDDReadRequest
from bdd_write_resquest import BDDWriteRequest

#Creation of class BDDWriteRequest
bbd_read_request = BDDReadRequest(conn, cur)
bbd_write_request = BDDWriteRequest(conn, cur)


# Import des fonctions de réponse websocket 
from websocket_management import server_message_event_to_specific_client, close_connection_to_specific_client


# le consomauteur fait office de controller
async def consumer_handler(queue: asyncio.Queue, client_webscocket=None):

    while True:
     
        # Attendez un élément de la queue
        message = await queue.get()
        controller(message)

        match message:
            case {'type': 'ready'}:
                print("message['type'] == 'ready'")
                bbd_write_request.isConnectedMscrapperDevice(message['model_id'], True)

            case {'type': 'scrapping_data'}:   
                  print()
                 # bbd_write_request.MscrapperLog(message['model_id'], "ready")
            case {'type': 'break'}:

                print("message['type'] == 'break'")
            case {'type': 'disconnect'}:
                close_connection_to_specific_client(message['device_id'], client_webscocket)


            case {'type': 'start_scrapping'}:
                print("message['type'] == 'start_scrapping'")


            case {'type': 'scrapping'}:

                print("message['type'] == 'disconnect'")
            case _:
                print("message['type'] == 'error'")

                
        # if(message['type'] == 'ready'):
        #     print("message['type'] == 'ready'")
        #     bbd_write_request.isConnectedMscrapperDevice(message['model_id'], True)

            #await server_message_event_to_specific_client(message['device_id'])
        #    pass
       # print("message: ", message)
        #print("bdd retour :", bbd_read_request.CheckMscrapperDevice())


 
        # Traitez le message ici
        print(f"Message consommé : {message}")
        queue.task_done()


async def producer_handler(message, queue: asyncio.Queue):
        
        #Ajout des ordres dans la queue
        print(json.loads(message))
        try : 
            await queue.put(json.loads(message))

        except Exception:
            print("Error dans le producer_handler json error")
        
       