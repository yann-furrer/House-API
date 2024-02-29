import threading
import time
from datetime import datetime
from controller.controller_management import *
import asyncio

print(bdd_read_request.GetWeekNumber())

#remplacer par une varibale vide
connected_list  = []
device_planning = {}



# compare every x second list of connected device in locally and in the bdd
# if the list is different, update monitoring.city_scrapping to assign the new connected device
def periodical_thread(device_list : list):
    #ajouter un eveneement pour envoyer aux autre tel si ils sont connecté

    requested_device_list = bdd_read_request.CheckMscrapperDevice()
    
    
    if  device_list != requested_device_list:
        print("new device connected detected")
        # met à jour le planning des scrappers
        global device_planning
        device_planning = assign_scrapers()

        global connected_list 
        connected_list = requested_device_list
   
    print("Fonction périodique exécutée")



def event_trigger(device_planning : object, queue: asyncio.Queue):

        while True:  # Boucle infinie pour vérifier continuellement
            now = datetime.datetime.now()
            for event_id, times in device_planning.items():
                for time_str in times:
                    time_obj = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
                    
                    # Comparer la date et l'heure, mais ignorer les secondes pour une comparaison plus générale
                    if time_obj.date() == now.date() and time_obj.hour == now.hour and time_obj.minute == now.minute:
                        print(f"Événement {event_id} déclenché à {time_str}")
                        queue.put(event_id)





def start_thread(interval):
    """Démarre la fonction périodique dans un thread séparé."""
    def tache():
        while True:
            periodical_thread(connected_list)
            time.sleep(interval)

    thread = threading.Thread(target=tache)
    thread.start()

# Démarrer la fonction périodique toutes les 30 secondes



