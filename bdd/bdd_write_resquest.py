from bdd.bdd_connector import conn, cur
from datetime import datetime

#Creation of class BDDWriteRequest
class BDDWriteRequest:
    #Constructor
    def __init__(self, conn, cur):
        self.connexion = conn
        self.cursor = cur


    #request monitoring.scrapper_log
    def MscrapperLog(self, model_id, type, success, task_id, website):
        try :
            self.cursor.execute(f"INSERT INTO monitoring.scrapper_log (add_date, model_id, type,  success, task_id , website) VALUES (CURRENT_TIMESTAMP, {model_id}, {model_id}, {success}, {task_id}, {website} );")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            print("Error in INSERT MscrapperLog")
            return False


    #request monitoring.scrapper_device
    def AddMscrapperDevice(self, model_id, is_connected=False ):
        #ajouter un check
        try:
            self.cursor.execute(f"INSERT INTO monitoring.scrapper_device (add_date, model_id, is_connected) VALUES (CURRENT_TIMESTAMP, '{model_id}', {is_connected});")
            self.conn.commit()
        except Exception as e:
            print(e)
            print("Error in INSERT MscrapperLog")


    # modify a state of is connected on monitoring.scrapper_device
    def isConnectedMscrapperDevice(self, model_id, is_connected=False ):
        #ajouter un check
        try:
            self.cursor.execute(f"UPDATE monitoring.scrapper_device SET add_date = CURRENT_TIMESTAMP, is_connected = {is_connected} WHERE model_id = '{model_id}';;")
            conn.commit()
        except Exception as e:
            print(e)
            print("Error in INSERT isConnectedMscrapperDevice")


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


    # pdate field id_scrapper to set the scraper_id 
    def UpdateScrapperPlanning(self, tuple_values):
        # try :
            update_query = f"""
        UPDATE monitoring.city_scraping
        SET id_scraper = %s
        WHERE id = %s;
        """
            self.cursor.executemany(update_query, tuple_values)
            conn.commit()
        # except Exception as e:
        #     print(e)
        #     print("Error in UPDATE UpdateScrapperPlanning")
