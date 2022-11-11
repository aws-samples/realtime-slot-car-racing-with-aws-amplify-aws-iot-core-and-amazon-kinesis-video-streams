import constants as constants
from mqtt_client import PahoMqttClient
from time import sleep
import random
from timeit import default_timer as timer

LOCAL_MQTT_ENDPOINT_HOST = "127.0.0.1"
LOCAL_MQTT_ENDPOINT_PORT = 1884


def handler(start_time):
    end = timer()
    print((end - float(start_time)) * 1000)


CALLBACK_CONFIG = {"test": handler}

client = PahoMqttClient(LOCAL_MQTT_ENDPOINT_HOST,
                        LOCAL_MQTT_ENDPOINT_PORT,
                        ['test'],
                        CALLBACK_CONFIG)
while 1 == 1:
    sleep(0.5)
    if client._connected == True:
        start = timer()
        ap_measurement = random.uniform(25.0, 150.0)
        client.send_payload(payload={"topic": "test", "payload": start})
    else:
        print("waiting for connection...")
