from bdd_connector import conn, cur
from datetime import datetime

#Creation of class BDDWriteRequest
class BDDWriteRequest:
    #Constructor
    def __init__(self, conn, cur):
        self.connexion = conn
        self.cursor = cur


    #request monitoring.scrapper_log
    def MscrapperLog(self, add_date, model_id, success, nb_data, website):
        try :
            self.cursor.execute(f"INSERT INTO monitoring.scrapper_log (add_date, model_id, success, nb_data, website) VALUES ({add_date}, {model_id}, {success}, {nb_data}, {website});")
            conn.commit()
        except Exception as e:
            print(e)
            print("Error in INSERT MscrapperLog")


    #request monitoring.scrapper_device
    def AddMscrapperDevice(self, add_date, model_id, is_connected=False ):
        #ajouter un check
        try:
            self.cursor.execute(f"INSERT INTO monitoring.scrapper_device (add_date, model_id, is_connected) VALUES ({add_date}, {model_id}, {is_connected});")
            conn.commit()
        except Exception as e:
            print(e)
            print("Error in INSERT MscrapperLog")


    # modify a state of is connected on monitoring.scrapper_device
    def isConnectedMscrapperDevice(self, add_date, model_id, is_connected=False ):
        #ajouter un check
        try:
            self.cursor.execute(f"INSERT INTO monitoring.scrapper_device (add_date, model_id, is_connected) VALUES ({add_date}, {model_id}, {is_connected});")
            conn.commit()
        except Exception as e:
            print(e)
            print("Error in INSERT MscrapperLog")


    # modify state and to an specific city
    def UpdateCityScityScrapping(self, commune_code, state, id_scraper, website):
        try :
            current_week = datetime.now().isocalendar()[1]
            today_date = datetime.now()
            formatted_date = today_date.strftime('%Y-%m-%d')
            self.cursor.execute(f"UPDATE monitoring.city SET state = {state}, week_number = {current_week}, scrape_date = {formatted_date} id_scraper = {id_scraper} WHERE commune_code = {commune_code};")
            conn.commit()
        except Exception as e:
            print(e)
            print("Error in UPDATE UpdateCityScityScrapping")