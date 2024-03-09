import asyncio
import websockets
import json

# Liste de requêtes de test
requetes_de_test = [
    {"type" : "ready", "device_id" : "postman"},
    {"type": "requete2", "data": "données2"},
    # Ajoutez d'autres requêtes selon les besoins
]

async def tester_websocket():
    uri = "ws://127.0.0.1:8765/ws?id=postman"  # Remplacez par l'URI approprié

    async with websockets.connect(uri) as websocket:
        for requete in requetes_de_test:
            # Envoyer une requête
            await websocket.send(json.dumps(requete))
            print(f"Requête envoyée: {requete.data}")

            # Attendre et afficher la réponse
            response = await websocket.recv()
            print(f"Réponse reçue: {response}")

# Exécuter la coroutine
asyncio.run(tester_websocket())
