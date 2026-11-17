import json
import random
import time
import uuid
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData
import os
from dotenv import load_dotenv

load_dotenv()


EVENTHUB_CONNECTION_STRING = os.getenv("EVENTHUB_CONNECTION_STRING")
EVENTHUB_NAME = os.getenv("EVENTHUB_NAME")

producer = EventHubProducerClient.from_connection_string(
    conn_str=EVENTHUB_CONNECTION_STRING,
    eventhub_name=EVENTHUB_NAME
)

STATION_IDS = ["ST001", "ST002", "ST003", "ST004", "ST005"]

VEHICLE_IDS = ["EV1001", "EV1002", "EV1003", "EV1004", "EV1005"]

CHARGING_STATUSES = ["Charging", "Completed", "Idle"]


def generate_telemetry():

    event = {
        "event_id": str(uuid.uuid4()),
        "station_id": random.choice(STATION_IDS),
        "vehicle_id": random.choice(VEHICLE_IDS),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "power_kw": round(random.uniform(5, 150), 2),
        "voltage": round(random.uniform(210, 250), 2),
        "current_amp": round(random.uniform(10, 250), 2),
        "energy_delivered_kwh": round(random.uniform(0, 100), 2),
        "battery_percentage": random.randint(10, 100),
        "charging_status": random.choice(CHARGING_STATUSES)
    }

    return event

try:
    while True:
        event_data = generate_telemetry()

        event_batch = producer.create_batch()
        event_batch.add(EventData(json.dumps(event_data)))

        producer.send_batch(event_batch)

        print(
            f"Sent event: {event_data['event_id']} | "
            f"Station: {event_data['station_id']} | "
            f"Status: {event_data['charging_status']}"
        )

        time.sleep(2)

except KeyboardInterrupt:
    print("Telemetry producer stopped.")

finally:
    producer.close()