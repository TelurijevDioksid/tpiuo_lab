import json
import asyncio
import requests
from azure.eventhub import EventHubProducerClient, EventData, EventDataBatch

connection_str = "Endpoint=sb://tr-ehns-tpiuo.servicebus \
    .windows.net/;SharedAccessKeyName=RootManageSharedAc \
    cessKey;SharedAccessKey=ALnbtW1QVgn/2FDqdM436WSSoW8/ \
    cL5dX+AEhMUQA28="
eventhub_name = "tr-eh-tpiou"
url = "https://oauth.reddit.com/r/dataengineering/top.json?limit=10&t=all"
auth = requests.auth.HTTPBasicAuth(
    "XlZ4O7CZJiuhBA4m46D9yw", "F2UQF2peItFRzFjaa2DLEULPLa2HUw"
)
data = {
    "grant_type": "password",
    "username": "ProfessionalStyle409",
    "password": "nagzu74$.,",
}
headers = {"User-agent": "tr:producer_app:v1.0 (by /u/Significant-Deal2472)"}
token_response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=auth,
    data=data,
    headers=headers,
)
token = token_response.json()["access_token"]
headers["Authorization"] = f"bearer {token}"


def add_to_batch(batch: EventDataBatch, after):
    params = {"after": after, "limit": 10}
    response = requests.get(url, headers=headers, params=params)
    print("Get response:")
    print(response)
    if response.ok:
        data = response.json()
        for post in data["data"]["childern"]:
            batch.add(EventData(json.dumps(post).encode("utf-8")))
        after = data["data"]["after"]
        return after
    return None


async def run():
    producer_client = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, eventhub_name=eventhub_name
    )
    after = None
    for _ in range(100):
        batch = producer_client.create_batch()
        after = add_to_batch(batch, after)
        print("Batch:")
        print(batch)
        if not after:
            break
        producer_client.send_batch(batch)
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(run())
    while True:
        continue
