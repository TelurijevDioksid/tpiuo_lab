import json

from azure.eventhub import EventHubConsumerClient

connection_str = "Endpoint=sb://tr-ehns-tpiuo.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=ALnbtW1QVgn/2FDqdM436WSSoW8/cL5dX+AEhMUQA28="
eventhub_name = "tr-eh-tpiou"
consumer_group = "$Default"

def on_event(partition_context, event):
    json_data = json.loads(event.body_as_str())
    print(json_data)
    partition_context.update_checkpoint(event)

consumer = EventHubConsumerClient.from_connection_string(
    connection_str, 
    consumer_group=consumer_group, 
    eventhub_name=eventhub_name
)

with consumer:
    consumer.receive(on_event=on_event)