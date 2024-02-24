#list of all read requests
from bdd_connector import conn, cur
import json

#Creation of class BDDWriteRequest
class BDDReadRequest:
    #Constructor
    def __init__(self, conn, cur):
        self.connexion = conn
        self.cursor = cur


    #return in json all id of scrapper devices and if is connected or not
    def CheckMscrapperDevice(self):
        try :
            self.cursor.execute(f"SELECT model_id, is_connected FROM monitoring.scrapper_device;")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT ChecKScrapperDevice")

        
    
    #return all logs of specific device in json
    def CheckSpecificModelIdMscrapperLog(self, model_id):
        try :
            self.cursor.execute(f"SELECT * FROM monitoring.scrapper_log WHERE model_id = {model_id};")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT CheckMscrapperLog")

    #return phase and xpath from a specifi website following phase 
    # It's data send to the scrapper to know where to click
    def GetDataMscrapperWebsite(self, website, phase):
        try :
            self.cursor.execute(f"SELECT phase, xpath, step, website FROM monitoring.scrapper_website WHERE phase = {phase} AND website_name = {website};")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetDataMscrapperWebsite")

    
    #return all city scrapped 
    def GetAllCityScityScrapping(self):
        try :
            self.cursor.execute(f"SELECT commune_code, city, id_scraper nb_rent, website, state FROM monitoring.city;")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetAllCity")

    #return all city to do
    def GetAllCityToDoScityScrapping(self):
        try :
            self.cursor.execute(f"SELECT commune_code, city, id_scraper nb_rent, website, state FROM monitoring.city WHERE state = 'TODO';")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetAllCity")