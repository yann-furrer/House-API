import json
import sys
import os
# Ajouter le chemin du dossier bdd
chemin_bdd = os.path.join(os.path.dirname(__file__), 'bdd')
if chemin_bdd not in sys.path:
    sys.path.append(chemin_bdd)

# Importation de la fonction ma_fonction de cd.py
from bdd_connector import conn, cur



from bdd_read_resquest import BDDReadRequest
def controller(queu_element ):
    print("controller")
    pass