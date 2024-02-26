
from itertools import cycle
from random import shuffle

import random
from datetime import datetime, timedelta
import os
import sys
# Ajouter le chemin du dossier bdd
# chemin_bdd = os.path.join(os.path.dirname(__file__), 'bdd')
# if chemin_bdd not in sys.path:
#     sys.path.append(chemin_bdd)

# Ajoute le répertoire parent au sys.path pour permettre les importations depuis d'autres sous-répertoires
chemin_du_repertoire_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if chemin_du_repertoire_parent not in sys.path:
    sys.path.append(chemin_du_repertoire_parent)

# Connexion à la base de données PostgreSQL
from bdd.bdd_connector import conn, cur
from bdd.bdd_read_resquest import BDDReadRequest
from bdd.bdd_write_resquest import BDDWriteRequest

bdd_read_request = BDDReadRequest(conn, cur)
bdd_write_request = BDDWriteRequest(conn, cur)




def clear_data_if_week_changed():
    # Obtenir le numéro de la semaine actuelle
    current_week = datetime.datetime.now().isocalendar()[1]
    
    # Vérifier le week_number dans la table    
    result = bdd_read_request.GetWeekNumber()

    if result != current_week:
        print(result)
        print("Les données ont été effacées en raison du changement de semaine.")
        return True
    else:
        print("Les données n'ont pas été effacées.")
        return False



def assign_scrapers():
   print(clear_data_if_week_changed())
   if( clear_data_if_week_changed()):
    #exemple of data device_connected_list [('test', False), ('postman', False)]
    scrapers = list([item[0] for item in bdd_read_request.CheckMscrapperDevice()]) 
    print(scrapers)

    scraper_cycle = cycle(scrapers)
    
    # Récupérer les villes à scraper
    cities = bdd_read_request.GetCityIdScrapping()
    
    # Mélanger aléatoirement la liste des villes pour varier la distribution
    shuffle(cities)

    # Préparation de la liste des mises à jour
    updates = []
    for city_id in cities:
        scraper_id = next(scraper_cycle)
        updates.append((scraper_id, city_id[0]))

    bdd_write_request.UpdateScrapperPlanning(updates)






def generer_horaires_aleatoires(ids:str, nb_time:int):
    horaires_par_id = {}
    for id in ids:
        horaires = []
        for _ in range(nb_time):  # Générer 5 horaires aléatoires par ID
            heure_random = random.randint(8, 17)  # Heure aléatoire entre 8h et 17h
            minute_random = random.randint(0, 59)  # Minute aléatoire
            # Créer l'horaire aléatoire pour aujourd'hui avec l'heure et la minute générées
            horaire = datetime.now().replace(hour=heure_random, minute=minute_random, second=0, microsecond=0)
            # Ajouter un délai aléatoire pour éviter les horaires exactement à l'heure pile
            horaire += timedelta(minutes=random.randint(1, 59))
            horaires.append(horaire.strftime("%Y-%m-%d %H:%M:%S"))
        horaires_par_id[id] = horaires
    return horaires_par_id

def random_break():
 #défini un temps de pause aléatoire en seoconde
  return random.randint(5, 10)

def random_product_click():
  #défini un nombre de clics aléatoire
  return random.randint(1, 5)
