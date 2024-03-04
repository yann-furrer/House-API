#list of all read requests
from bdd.bdd_connector import conn, cur
import json
import os 
import sys

#Creation of class BDDWriteRequest
class BDDReadRequest:
    #Constructor
    def __init__(self, conn, cur):
        self.connexion = conn
        self.cursor = cur


    # return in json all id of scrapper devices and if is connected or not
    def CheckMscrapperDevice(self):
      #  try :
            print("passe dans la requete")
            self.cursor.execute(f"SELECT model_id, is_connected FROM monitoring.scrapper_device;")
           # print(self.cursor.fetchall()[ø])
            #print(json.dumps(self.cursor.fetchall()))
            return self.cursor.fetchall()
        # except Exception as e:
        #     print(e)
        #     print("Error in SELECT ChecKMScrapperDevice")

        
    
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

    
    #return last 3 logs of every device from dynamic view in monitoring 
    def GetLastLogs(self):
        try :
            self.cursor.execute(f"SELECT * FROM monitoring.scrapper_log;")
            #print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetLastLogs")


    # Return all city's id to scrapping step from city_scrapping
    def GetCityIdScrapping(self):
       # try :
            self.cursor.execute(f"SELECT id FROM monitoring.city_scraping WHERE state = 'TODO';")
            #print(json.dumps(self.cursor.fetchall()))
            #return json.dumps(self.cursor.fetchall())
            return self.cursor.fetchall()
       # except Exception as e:
        #    print(e)
        #    print("Error in SELECT GetCityScrappingStep")     

    # return week number of table city_scraping
    def GetWeekNumber(self):
        try :
            self.cursor.execute(f"SELECT week_number FROM monitoring.city_scraping  ORDER BY id LIMIT 1 ;")
            #print(self.cursor.fetchall()[0][0])
            # return value of first row week_number
            return self.cursor.fetchall()[0][0]
        except Exception as e:
            print(e)
            print("Error in SELECT GetWeekNumber")   

