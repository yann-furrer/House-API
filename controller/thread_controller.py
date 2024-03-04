import threading
import time
from datetime import datetime
from controller.controller_management import *
import asyncio
import queue
#remplacer par une varibale vide
connected_list  = []
device_planning = {}


def event_trigger_testing(device_planning : object, queue_event: queue.Queue):
    print("__event_trigger__testing")
    event_id = "ceci est un test" 
    time_str = "2021-10-10 10:10:10"      
    print(f"Événement {event_id} déclenché à {time_str}")
    queue_event.put(event_id)
    queue_event.put({'type': 'sleep'})

# compare every x second list of connected device in locally and in the bdd
# if the list is different, update monitoring.city_scrapping to assign the new connected device
def periodical_thread(connected_list : list, device_planning : object, queue_event: queue.Queue):
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

            #print(device_planning, "device_planning2")
            connected_list = requested_device_list
    
        print("Fonction périodique exécutée")
        time.sleep(10)



def event_trigger(device_planning : object, queue_event: queue.Queue):
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

                    queue_event.put({'type': 'sleep'})







