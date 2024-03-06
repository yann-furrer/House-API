import threading
import time
from datetime import datetime
from controller.controller_management import *
import asyncio

import uuid
#remplacer par une varibale vide
connected_list  = []
device_planning = {}


async def event_trigger_testing(device_planning : object, queue_event: asyncio.Queue):
    print("__event_trigger__testing")
    event_id = "ceci est un test" 
    time_str = "2021-10-10 10:10:10"      
    print(f"Événement {event_id} déclenché à {time_str}")
    await queue_event.put(event_id)
    await queue_event.put({'type': 'sleep'})

# compare every x second list of connected device in locally and in the bdd
# if the list is different, update monitoring.city_scrapping to assign the new connected device
async def periodical_thread(connected_list : list, device_planning : object, queue_event: asyncio.Queue):
    print("__periodical_thread__")
    #ajouter un eveneement pour envoyer aux autre tel si ils sont connecté
    while True:
        #event_trigger_testing(device_planning, queue_event)
        requested_device_list = bdd_read_request.CheckMscrapperDevice()
        
        
        if  connected_list != requested_device_list:
            print("new device connected detected")
            # met à jour le planning des scrappers
            #print(device_planning, "device_planning")

            device_planning = assign_scrapers()
            print(device_planning)
            #print(device_planning, "device_planning2")
            connected_list = requested_device_list
    
        print("Fonction périodique exécutée")
        await asyncio.sleep(10)


    #         'type': 'emit',
    #         'time': datetime.datetime.utcnow().isoformat(),
    #         'phase': 'launch'
    #         'url' 'url',
    #         'xpath_sequence': ["séquence une xppath", "séquence deux xpath", "séquence trois xpath"],
    #         'data': 'data is comming!',
    #         'device_id' : id,
    #         'city': 'city',
    #         'price_limit': 'price_limit',
    #         'ban words' : 'ban words'
async def event_trigger(device_planning : object, queue_event: asyncio.Queue):
        print("__event_trigger__")
        while True:  # Boucle infinie pour vérifier continuellement
            now = datetime.now()
            for event_id, times in device_planning.items():
                for time_str in times:
                    time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
                    
                    # Comparer la date et l'heure, mais ignorer les secondes pour une comparaison plus générale
                    if time_obj.date() == now.date() and time_obj.hour == now.hour and time_obj.minute == now.minute:
                        print(f"Événement {event_id} déclenché à {time_str}")
                        queue_event.put(event_id)
                        print('event id in event trigger',event_id)

                        #get city name in tuple  
                        random_city = bdd_read_request.GetRandomCity(event_id)[0][1]
                        xpath_array = bdd_read_request.GetXpath()
                        xpath_array = [item[0] for item in xpath_array]
                        print(xpath_array)
                        # génère un identifiant unique lié à la tache de scrapping 
                        task_id = uuid.uuid4()
                        url =  bdd_read_request.GetUrl()[0]
                        queue_event.put({'type': 'start_scrapping', 'url'  : url+'+'+random_city, 'task_id': task_id, 'xpath_sequence': xpath_array, 'city': random_city ,'price_limit': 300, 'ban words' : ['bitcoin']})







