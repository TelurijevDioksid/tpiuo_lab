import requests
import json
from azure.eventhub import EventHubProducerClient, EventData

connection_str = "Endpoint=sb://tr-ehns-tpiuo.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ALnbtW1QVgn/2FDqdM436WSSoW8/cL5dX+AEhMUQA28="
eventhub_name = "tr-eh-tpiou"
url = "https://oauth.reddit.com/r/dataengineering/top.json?limit=10&t=all"
auth = requests.auth.HTTPBasicAuth(
    "XlZ4O7CZJiuhBA4m46D9yw",
    "F2UQF2peItFRzFjaa2DLEULPLa2HUw"
)
data = {
    "grant_type": "password",
    "username": "ProfessionalStyle409",
    "password": "nagzu74$.,"
}
headers = {
    "User-agent": "tr:producer_app:v1.0 (by /u/Significant-Deal2472)"
}

token_response = requests.post(
    "https://www.reddit.com/api/v1/access_token", 
    auth=auth,
    data=data,
    headers=headers
)
token = token_response.json()["access_token"]
headers["Authorization"] = f"bearer {token}"

posts_response = requests.get(url, headers=headers)
data = posts_response.json()

producer = EventHubProducerClient.from_connection_string(connection_str, eventhub_name=eventhub_name)

event_data_batch = producer.create_batch()
for post in data["data"]["children"]:
    event_data_batch.add(EventData(json.dumps(post["data"])))
producer.send_batch(event_data_batch)

while True:
    pass