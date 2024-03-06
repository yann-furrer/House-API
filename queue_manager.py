# Description: Ce fichier contient les fonctions qui permettent de gérer la queue
#from controller.controller import controller
import asyncio
import json
import time
import sys
import os
import random



# Ajouter le chemin du dossier bdd
chemin_bdd = os.path.join(os.path.dirname(__file__), 'bdd')
if chemin_bdd not in sys.path:
    sys.path.append(chemin_bdd)

# Importation des fonctions d'écriture et de lecture de la base de données
from bdd_connector import conn, cur
from bdd_read_resquest import BDDReadRequest
from bdd_write_resquest import BDDWriteRequest
import queue
#Creation of class BDDWriteRequest
bdd_read_request = BDDReadRequest(conn, cur)
bdd_write_request = BDDWriteRequest(conn, cur)


# Import des fonctions de réponse websocket 
from websocket_management import send_message_to_specific_client, close_connection_to_specific_client





# le consommateur gérè l'ensemble des evenements sauf le depart et la planning
async def consumer_handler(queue_event: asyncio.Queue, clients: object):


#ajouter un générateur de task id

    print("__controller ok__")
    while True:
     
        # Attendez un élément de la queue
        message = await queue_event.get()
        
        print("message consummer: ", message)

        match message:
            # First connection
            case {'type': 'first_connection'}:
                try :
                    print("message['type'] == 'first_connection'")

                    bdd_write_request.AddMscrapperDevice(message['model_id'], True)
                    json_message = json.dumps({'type': 'first_connection', 'device_id': message['device_id'], 'date': time.time(), 'state': '200', 'info': "first connection event succed", "task_id" :  message['task_id']})
                    await send_message_to_specific_client(message['device_id'], clients,json_message)
                    #Ajout de l'evenement dans les logs
                    bdd_write_request.MscrapperLog( message['model_id'], "first_connection" ,200 ,message["task_id"])
                except Exception as error:

                    
                    await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'first_connection', 'device_id': message['device_id'], 'date': time.time(), 'state': '400', 'info': error, "task_id" :  message['task_id']}))
                    #Ajout de l'evenement dans les logs
                    bdd_write_request.MscrapperLog( message['model_id'], "first_connection" ,200 ,message["task_id"])
                    print("Error dans le consumer_handler")



            case {'type': 'ready'}:
                print("message['type'] == 'ready'")
                bdd_write_request.isConnectedMscrapperDevice(message['model_id'], True)
                send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'ready', 'device_id': message['device_id'], 'date': time.time(), 'state': '200', 'info': error, "task_id" :  message['task_id']}))

            case {'type': 'scrapping_data'}:   
                  print("message['type'] == 'scrapping_data'")
                 # bbd_write_request.MscrapperLog(message['model_id'], "ready")
            
            case {'type': 'disconnect'}:
                close_connection_to_specific_client(message['device_id'], clients)


            case {'type': 'start_scrapping'}:
                print("message['type'] == 'start_scrapping'")
                json_message = {'type', 'start_scrapping'}

            case {'type': 'test'}:
                print("message['type'] == 'test'")
                json_message = {'type', 'start_scrapping'}
                await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'test', 'device_id': message['device_id'], 'date': time.time(), 'state': '200', 'info': 'test ok succes'}))
            
    #         



                
                print(message)

            # Pause dans le processsus entre 1 et 5 minutes
            case {'type': 'sleep'}:

                sleep_time = random.randint(5, 300)
                send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'sleep', 'device_id': message['device_id'], 'date': time.time(), 'state': '200', 'info': sleep_time, "task_id" :  message['task_id']}))
                #Ajout de l'evenement dans les logs
                bdd_write_request.MscrapperLog( message['model_id'], "sleep" ,200 ,message["task_id"])
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
        queue_event.task_done()


async def producer_handler(message, queue_event: asyncio.Queue):
        
        #Ajout des ordres dans la queue
        print(json.loads(message))
       # try : 
        await queue_event.put(json.loads(message))

       # except Exception:
       #     print("Error dans le producer_handler json error")
        
       