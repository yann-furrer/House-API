import sys
from datetime  import datetime
import uuid
import asyncio

random_id = uuid.uuid4()
a = asyncio.Queue() 
async def test_request(queue_event: asyncio.Queue):
    if '-test' in sys.argv:
            # Si oui, créez une liste d'événements de test et ajoutez-les dans la queue
            test_events = [{'type': 'start_scrapping','date': str(datetime.now()) ,'device_id' : "cacahd",'url'  : 'https://www.google.com/search?q=seloger.com+'+'+bordeaux', 'task_id': "rrrkjrkfhkjr", 'xpath_sequence': 'xpath_array', 'city': 'bordeaux' ,'price_limit': 300, 'ban words' : ['bitcoin'], "website" : "seloger" }
                        
                        ]
            for event in test_events:
                print(event)
                await asyncio.sleep(20)
                await queue_event.put(event)

