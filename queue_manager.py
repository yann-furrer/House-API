import asyncio
import json
import os
import random
import sys
from datetime import datetime
from bdd.bdd_connector import conn, cur
from bdd.bdd_read_resquest import BDDReadRequest
from bdd.bdd_write_resquest import BDDWriteRequest
from websocket_management import send_message_to_specific_client, close_connexion_to_specific_client

# Ajout du chemin du dossier bdd
chemin_bdd = os.path.join(os.path.dirname(__file__), 'bdd')
if chemin_bdd not in sys.path:
    sys.path.append(chemin_bdd)

# Initialisation des requêtes de base de données
bdd_read_request = BDDReadRequest(conn, cur)
bdd_write_request = BDDWriteRequest(conn, cur)

# Gestionnaire de consommateur : gère tous les événements sauf le départ et la planification
async def consumer_handler(queue_event: asyncio.Queue, clients: dict):
    print("__controller ok__")
    while True:
        message = await queue_event.get()
        print("message consummer: ", message)
        try:
            # Gestion des types de messages avec des fonctions dédiées
            handler = MESSAGE_HANDLERS.get(message['type'])
            if handler:
                await handler(message, clients, queue_event)
            else:
                print(f"Type de message inconnu : {message['type']}")
                await send_message_to_specific_client(message['device_id'], clients, json.dumps({'type': message['type'], 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "type inconu"}))
        except Exception as error:
            print(f"Erreur dans le gestionnaire de consommateur : {error}")
        finally:
            queue_event.task_done()







# Gestionnaire de producteur : ajoute des messages à la file d'attente
async def producer_handler(message: str, queue_event: asyncio.Queue):
    try:
        await queue_event.put(json.loads(message))
        print(f"Message ajouté à la queue : {json.loads(message)}")
    except json.JSONDecodeError:
        print("Erreur de décodage JSON dans le gestionnaire de producteur")




# Générateur de tâches : crée des tâches de consommateur et de producteur
# Handlers spécifiques pour chaque type de message
        
async def handle_first_connexion(message: dict, clients: dict, queue_event: asyncio.Queue):
    # Cette fonction gère les événements de première connexion
    print("first connexion")
    print(bdd_read_request.CheckMscrapperOneDevice(message['device_id']))
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == True:
        print("first connexion passe")
        
        json_message = json.dumps({'type': 'first_connexion', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "first connexion failed , this id alrready exist in db, use ready instead"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        print("----------------", message['device_id'])
        
        bdd_write_request.MscrapperLog( message['device_id'], "first_connexion" ,False ,"NULL", "NULL")
        #raise Exception("Un appareil existe déjà dans la bdd avec cet id")
    else:
        bdd_write_request.AddMscrapperDevice(message['device_id'], True)
        # En cas d'échec, envoie un message d'erreur au client
        json_message = json.dumps({'type': 'first_connexion', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 200, 'info': "first connexion event succed new device added to db"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        #Ajout de l'evenement dans les logs
        bdd_write_request.MscrapperLog( message['device_id'], "first_connexion" ,True ,"NULL", "NULL")



async def handle_ready(message: dict, clients: dict, queue_event: asyncio.Queue):
    # Cette fonction gère les événements de prêt et met le champ 'is_connected' à True
    
        # En cas d'échec, envoie un message d'erreur au client
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == False:
        bdd_write_request.isConnectedMscrapperDevice(message['device_id'], True)
        json_message = json.dumps({'type': 'ready', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': '400', 'info': "ready failed device not found in db, use first_connexion instead"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        raise Exception("Erreur dans la mise à jour de l'appareil")
    await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'ready', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': '200', 'info': "Device is ready", }))



async def handle_disconnect(message: dict, clients: dict, queue_event: asyncio.Queue):
    # Cette fonction gère les événements de déconnexion
    print("--___>", bdd_read_request.CheckMscrapperOneDevice(message['device_id']))
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == False:
        # En cas d'échec, envoie un message d'erreur au client
        bdd_write_request.isConnectedMscrapperDevice(message['device_id'])
        json_message = json.dumps({'type': 'disconnect', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "disconnect clean connexion failed device_id not found in db"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        bdd_write_request.MscrapperLog( message['device_id'], "disconnect" ,False ,"NULL", "NULL")

        raise Exception("Erreur dans la mise à jour de l'appareil")
    else :
        # En cas de succès, envoie un message de déconnexion au client
        json_message = json.dumps({'type': 'disconnect', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 200, 'info': "disconnect clean connexion ok "})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        await close_connexion_to_specific_client(message['device_id'], clients)
        bdd_write_request.MscrapperLog( message['device_id'], 'disconnect' ,True ,"NULL", "NULL")
        del clients[message['device_id']]



async def handle_test(message: dict, clients: dict, queue_event: asyncio.Queue):
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == False:
        # En cas d'échec, envoie un message d'erreur au client
        json_message = json.dumps({'type': 'test', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "test failed device_id not found in db"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        raise Exception("Erreur dans le test de l'appareil")
    else :
        # Cette fonction gère les événements de test
        await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'test', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': '200', 'info': 'test ok succes'}))



async def handle_break(message: dict, clients: dict, queue_event: asyncio.Queue ):
    # Cette fonction gère les événements de pause
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == False:
        # En cas d'échec, envoie un message d'erreur au client
        json_message = json.dumps({'type': 'break', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "break failed device_id not found in db"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        bdd_write_request.MscrapperLog( message['device_id'], "break" ,True ,message["task_id"], "NULL")
        raise Exception("Erreur dans la mise à jour de l'appareil")
    else :
        break_time = random.randint(5, 300)
        await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'break', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 200, 'break': break_time, "task_id" :  message['task_id']}))            #Ajout de l'evenement dans les logs
        bdd_write_request.MscrapperLog( message['device_id'], "break" ,True ,message["task_id"], "NULL")



async def handle_sleep(message: dict, clients: dict, queue_event: asyncio.Queue):
    # Cette fonction gère les événements de pause
    if bdd_read_request.CheckMscrapperOneDevice(message['device_id']) == False:
        # En cas d'échec, envoie un message d'erreur au client
        json_message = json.dumps({'type': 'sleep', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "sleep failed device_id not found in db"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        bdd_write_request.MscrapperLog( message['device_id'], "sleep" ,True ,message["task_id"], "NULL")
        raise Exception("Erreur dans la mise à jour de l'appareil")

    else:
        # En cas de succès, envoie un message de pause au client
        bdd_write_request.MscrapperLog( message['device_id'], "sleep" ,True ,message["task_id"], "NULL")
        await send_message_to_specific_client(message['device_id'], clients,json.dumps({'type': 'sleep', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 200, 'info': 'sleep ok succes', 'website': 'https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-unique-constraint/' }))



async def handle_start_scrapping(message: dict, clients: dict, queue_event: asyncio.Queue):
    # Cette fonction gère les événements de lancement
    print("start scrapping")
    print(message)
    bdd_write_request.MscrapperLog( message['device_id'], "start_scrapping" ,True ,message["task_id"], message["website"])
    await send_message_to_specific_client(message["device_id"], clients, json.dumps({'type': 'test','date' : message["date"], 'url'  : message['url'], 'task_id': message['task_id'], 'xpath_sequence': message['xpath_sequence'], 'city': message['city'] ,'price_limit':  message['price_limit'], 'ban words' : ['bitcoin']}))



async def handle_scrapping_data(message: dict, clients: dict, queue_event: asyncio.Queue):
    print("data -----------")
    print(message)
    if len(message["data"]) == 0:
        # En cas d'échec, envoie un message d'erreur au client
        json_message = json.dumps({'type': 'scrapping_data', 'device_id': message['device_id'], 'date': str(datetime.now()), 'state': 400, 'info': "scrapping data failed"})
        await send_message_to_specific_client(message['device_id'], clients,json_message)
        raise Exception("Erreur dans le scraping  de l'appareil")
    else:
        print("appel de la fonction qui traite les data")
    # Cette fonction gère les événements de scrapping
        bdd_write_request.MscrapperLog(message['device_id'], "scrapping_data" ,True ,"NULL", "NULL")
    #mettre en mode break pour savoir si y'a une pause et pareil pour les clicks
        queue_event.put(json.load({"type": "scrapping_data", "device_id": message['device_id'], "date": str(datetime.now()), "state": 200, "info": "sleep ok succes", "website": "https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-unique-constraint/"}))

# Mapping des gestionnaires en fonction du type de message
MESSAGE_HANDLERS = {
    'first_connexion': handle_first_connexion,
    'ready': handle_ready,
    'disconnect': handle_disconnect,
    'test': handle_test,
    'break': handle_break,
    'sleep': handle_sleep,
    'start_scrapping': handle_start_scrapping,
    'scrapping_data': handle_scrapping_data
    # Ajoutez d'autres mappings ici
}

