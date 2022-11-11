import utils.constants as constants

import paho.mqtt.client as mqtt
import ssl

from utils.client import Client

class MqttClient(Client):
    def __init__(self, id, client, connection_options, topics, callback_config, client_type) -> None:
        super().__init__(client_type=client_type)
        self._topics = topics
        self._mainTopic = self._topics[0]

        self.client = client
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        self.client.on_connect = self.on_connect
        self.id = id

        self.connection_options = connection_options
        self.callback_config = callback_config

        self.connect()

        self.client.loop_start()

    def connect(self):
        try:
            self.client.connect(
                self.connection_options.get("host"),
                port=self.connection_options.get("port"),
                keepalive=60
            )
        except Exception as e:
            print("Error connecting: ", e)

    def on_publish(self, client, userdata, mid):
        print(userdata + " -- " + mid)

    def on_message(self, client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        callback_function = self.callback_config.get(msg.topic)
        if callback_function is not None:
            callback_function(msg.payload)


    def on_connect(self, client, userdata, flags, rc):
        print(f"Successfully connected to {self.id} - {self.connection_options.get('host')}")
        self._connected = True

        array_of_topic_tuples = [(topic, 0) for topic in self._topics]

        self.client.subscribe(array_of_topic_tuples)

    def send_payload(self, payload):
        topic = payload.get('topic')
        message_string = payload.get('message_string')

        if (self._connected == False):
            self.connect()
        try:
            self.client.publish(topic, message_string, qos=0, retain=False)
        except Exception as e:
            print("Error sending message: ", e)

    def on_subscribe(client, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_disconnect(self, client, userdata, rc):
        client.disconnect()
        client.loop_stop()
        self._connected = False


class PahoMqttClient(MqttClient):
    def __init__(self, id, host, port, topics, callback_config) -> None:
        connection_options = {
            "host": host,
            "port": port
        }
        client = mqtt.Client()
        is_remote = host == constants.MOSQUITTO_TEST_MQTT_ENDPOINT_HOST
        client_type = constants.CLIENT_OPTIONS["REMOTE_MQTT"] if is_remote else constants.CLIENT_OPTIONS["LOCAL_MQTT"]
        super().__init__(id, client, connection_options, topics, callback_config, client_type)


class IoTCoreMqttClient(MqttClient):
    def __init__(self, id, host, port, topics, callback_config) -> None:
        connection_options = {
            "host": host,
            "port": port
        }

        client = mqtt.Client("TestThing")
        ca_path = "utils/certificate/AmazonRootCA1.pem"
        cert_path = "utils/certificate/aws_cert.pem.crt"
        private_key_path = "utils/certificate/private.pem.key"

        client.tls_set(
            ca_path,
            certfile=cert_path,
            keyfile=private_key_path,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None
        )
        client_type = constants.CLIENT_OPTIONS["IOT_CORE"]
        super().__init__(id, client, connection_options, topics, callback_config, client_type)
