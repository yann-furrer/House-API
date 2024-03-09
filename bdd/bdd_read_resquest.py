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

    # return if scraper is in the database
    def CheckMscrapperOneDevice(self, model_id: str):
        try :
            print("passe dans la requete")
            self.cursor.execute(f"SELECT model_id FROM monitoring.scrapper_device WHERE model_id ='{model_id}';")
            #return false si la requete est vide
            return True if self.cursor.fetchall() else False
        except Exception as e:
             print(e)
             print("Error in SELECT CheckMscrapperOneDevice")



    # return in json all id of scrapper devices and if is connected or not
    def CheckMscrapperDevice(self):
        try :
            print("passe dans la requete")
            self.cursor.execute(f"SELECT model_id, is_connected FROM monitoring.scrapper_device;")
           # print(self.cursor.fetchall()[ø])
            #print(json.dumps(self.cursor.fetchall()))
            return self.cursor.fetchall()
        except Exception as e:
             print(e)
             print("Error in SELECT ChecKMScrapperDevice")

        
    
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
            self.cursor.execute(f"SELECT commune_code, city, id_scraper nb_rent, website, state FROM monitoring.city_scraping;")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetAllCity")

    #return all city to do
    def GetAllCityToDoScityScrapping(self):
        try :
            self.cursor.execute(f"SELECT commune_code, city, id_scraper nb_rent, website, state FROM monitoring.city_scraping WHERE state = 'TODO';")
            print(json.dumps(self.cursor.fetchall()))
            return json.dumps(self.cursor.fetchall())
        except Exception as e:
            print(e)
            print("Error in SELECT GetAllCity")
    
    #return a random city to do from monitoring.city
    def GetRandomCity(self, id_scraper: str):
        try :
            self.cursor.execute(f"SELECT commune_code, city FROM monitoring.city_scraping WHERE state = 'TODO' AND id_scraper = '{id_scraper}' ORDER BY RANDOM() LIMIT 1;")
            #print(json.dumps(self.cursor.fetchall()))
            #return json.dumps(self.cursor.fetchall())
            return self.cursor.fetchall()
        except Exception as e:
            print(e)
            print("Error in SELECT GetRandomCity")


    
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

    # return xpath for selected Wokflow id 
    def GetXpath(self, workflow_id=2):
        try:
            self.cursor.execute(f"SELECT xpath_website FROM monitoring.scrapper_website  WHERE id_workflow = '2' ;")
            return self.cursor.fetchall()
        except Exception as e:
           print(e)
           print("Error in SELECT GetXpath")


    # return first url to strart scraping 
    def GetUrl(self):
        try:
            self.cursor.execute(f"SELECT url FROM monitoring.scrapper_website  WHERE id_workflow = '2' ORDER BY step ASC LIMIT 1;")
            return self.cursor.fetchall()
        except Exception as e:
           print(e)
           print("Error in SELECT GetUrl")


