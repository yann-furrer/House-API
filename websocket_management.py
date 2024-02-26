
from urllib.parse import urlparse, parse_qs
from handle_error import IsId
import datetime
import json







async def close_connection_to_specific_client(id, clients):
    client_websocket = clients[id]
    await client_websocket.send(f"Fermeture de la connexion du client ${id}")
    await client_websocket.close()
    del clients[id]


async def server_message_event_to_specific_client(id, clients):
    client_id = clients[id]
    event_data = {
            'type': 'emit',
            'time': datetime.datetime.utcnow().isoformat(),
            'phase': 'launch'
            'url' 'url',
            'xpath_sequence': ["séquence une xppath", "séquence deux xpath", "séquence trois xpath"],
            'data': 'data is comming!',
            'device_id' : id,
            'city': 'city',
            'price_limit': 'price_limit',
            'ban words' : 'ban words'
        }
        
        # Convert the event data to a JSON string to send
    event_message = json.dumps(event_data)

    # dans ce cas client_id est un websocket
    await client_id.send(event_message)