# queue_manager.py

import asyncio
import json
import time
async def consumer_handler(queue: asyncio.Queue):

    while True:
        time.sleep(1)
        # Attendez un élément de la queue
        message = await queue.get()

        print(f"Message consommé : {message}")
        # Traitez le message ici
        print(f"Message consommé : {message}")
        queue.task_done()


async def producer_handler(message, queue: asyncio.Queue):
        
        #Ajout des ordres dans la queue
        await queue.put(json.loads(message))
        
       