import json
import sys
import os
import threading
import time
from datetime import datetime
import asyncio
# Ajoute le répertoire parent au sys.path pour permettre les importations depuis d'autres sous-répertoires
chemin_du_repertoire_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if chemin_du_repertoire_parent not in sys.path:
    sys.path.append(chemin_du_repertoire_parent)

#importation des threads et des fonctions pour le controller
from controller.thread_controller import periodical_thread, assign_scrapers, event_trigger, start_thread, connected_list, device_planning

# Importation des fonctions d'écriture et de lecture de la base de données
from bdd.bdd_connector import conn, cur
from bdd.bdd_read_resquest import BDDReadRequest



bbd_read_request = BDDReadRequest(conn, cur)


def controller_e(queu_message: asyncio.Queue):
    """Démarre la fonction périodique dans un thread séparé."""
    start_thread(5)