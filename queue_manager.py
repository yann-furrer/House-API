# queue_manager.py
from controller import controller
import asyncio
import json
import time
async def consumer_handler(queue: asyncio.Queue):

    while True:
        time.sleep(1)
        # Attendez un élément de la queue
        message = await queue.get()
        isSucess = controller()
        print(isSucess)
        print(f"Message consommé : {message}")
        # Traitez le message ici
        print(f"Message consommé : {message}")
        queue.task_done()


async def producer_handler(message, queue: asyncio.Queue):
        
        #Ajout des ordres dans la queue
        await queue.put(json.loads(message))
        
       