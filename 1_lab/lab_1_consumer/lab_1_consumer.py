import json
from typing import List
from azure.eventhub import EventHubConsumerClient, EventData
from datetime import datetime
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core.exceptions import ResourceNotFoundError

connection_str = "Endpoint=sb://tr-ehns-tpiuo.servicebus.windows \
    .net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAc \
    cessKey=ALnbtW1QVgn/2FDqdM436WSSoW8/cL5dX+AEhMUQA28="
eventhub_name = "tr-eh-tpiou"
consumer_group = "$Default"
storage_account_name = "trredditstorage"
storage_container_name = "trredditcontainer"
storage_account_connection_str = "DefaultEndpointsProtocol=https; \
    AccountName=trredditstorage;AccountKey=Xvd5NsR3V6YSo68+CY2kRS \
    pR08qKCpYjsuJ1KG4M+85FfNZ234n/2cEUGg39WBWCeFE1Pkgpem/B+AStgf2 \
    m4w==;EndpointSuffix=core.windows.net"

data_lake_service_client = DataLakeServiceClient.from_connection_string(
    conn_str=storage_account_connection_str
)

file_system_client = data_lake_service_client.get_file_system_client(
    file_system=storage_container_name
)


def on_event_batch(pc, events: List[EventData]):
    file_counter = 0
    for event in events:
        post = json.loads(event.body_as_str(encoding="UTF-8"))
        creation = post["data"]["created_utc"]
        creation_date = datetime.utcfromtimestamp(creation)
        bucket_client = file_system_client.get_directory_client(
            f"{creation_date.year}/{creation_date.month}/"
            f"{creation_date.day}/{creation_date.hour}"
            f"/{creation_date.minute}"
        )
        try:
            dir_props = bucket_client.get_directory_properties()
            print("Found bucket: " + dir_props.name)
        except ResourceNotFoundError:
            bucket_client.create_directory()
            new_bucket = bucket_client.get_directory_properties()
            print("New bucket: " + new_bucket.name)
        file_client = bucket_client.get_file_client(str(file_counter))
        file_client.create_file()
        event_b = str(event).encode("utf-8")
        event_b_len = len(event_b)
        file_client.append_data(event_b, 0, event_b_len)
        file_client.flush_data(event_b_len)
        file_counter += 1


if __name__ == "__main__":
    event_hub_consumer_client = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group, eventhub_name=eventhub_name
    )
    with event_hub_consumer_client:
        event_hub_consumer_client.receive_batch(on_event_batch=on_event_batch)
