import asyncio
import websockets


async def IsId(websocket, client_id):

    if not client_id or client_id.isdigit():
        print("bad id ")
        #asyncio.create_task(websocket.close(code=1002, reason="Invalid ID"))
        await websocket.send("Fermeture bad id")
        await websocket.close(code=1002, reason="Invalid ID")

        return False
    else:
        return True

