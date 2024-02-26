import json
import sys
import os

# Ajoute le répertoire parent au sys.path pour permettre les importations depuis d'autres sous-répertoires
chemin_du_repertoire_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if chemin_du_repertoire_parent not in sys.path:
    sys.path.append(chemin_du_repertoire_parent)


# Importation des fonctions d'écriture et de lecture de la base de données
from bdd.bdd_connector import conn, cur
from bdd.bdd_read_resquest import BDDReadRequest



bbd_read_request = BDDReadRequest(conn, cur)


def controller(queu_message ):
    print("controller:", queu_message)


    #exemple of data device_connected_list [('test', False), ('postman', False)]
    device_connected_list = bbd_read_request.CheckMscrapperDevice()
    las_log_by_device = bbd_read_request.GetLastLogs()
    
    print("device_connected_list", device_connected_list)
    print("las_log_by_device", las_log_by_device)
    #bbd_read_request.CheckMscrapperDevice("postman")

print(controller("test"))