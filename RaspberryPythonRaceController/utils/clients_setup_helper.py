import utils.constants as constants
import utils.mqtt_client as mqtt_client

class ClientsSetupHelper():
    def __init__(self, racerHelper) -> None:
        self.car_and_race_update_client = None
        self.slot_car_update_client = None

        # raceAndCarClientSetting = constants.CAR_AND_RACE_UPDATE_CLIENT
        slotcarsClientSetting = constants.slot_car_update_client

        mqttHelper = MQTTClientSetupHelper(racerHelper)

        if mqttHelper.car_and_race_update_client:
            self.car_and_race_update_client = mqttHelper.car_and_race_update_client
        if mqttHelper.slot_car_update_client:
            self.slot_car_update_client = mqttHelper.slot_car_update_client
        if slotcarsClientSetting == constants.CLIENT_OPTIONS["SERIAL"]:
            from utils.serial_client import SerialClient
            self.slot_car_update_client = SerialClient()
        if slotcarsClientSetting == constants.CLIENT_OPTIONS["USB"]:
            from utils.usb_client import USBClient
            self.slot_car_update_client = USBClient()


class MQTTClientSetupHelper:
    def __init__(self, racerHelper) -> None:
        self.car_and_race_update_client = None
        self.slot_car_update_client = None

        self.slot_cars_handler = racerHelper.handleRaceTrackData
        self.car_update_handler = racerHelper.handleCarUpdate
        self.race_update_handler = racerHelper.handleRaceUpdate

        print("Car and Race client: " + constants.CAR_AND_RACE_UPDATE_CLIENT)
        print("Slot cars client: " + constants.slot_car_update_client)

        self.callback_config_car_and_race = {
            constants.CAR_CONTROL_UPDATE_TOPIC: self.car_update_handler,
            constants.GAME_STATE_UPDATE_TOPIC: self.race_update_handler,
        }

        self.callback_config_slot_cars = {
            constants.TRACK_MQTT_TOPIC_NAME_SUB: self.slot_cars_handler,
        }

        if constants.CAR_AND_RACE_UPDATE_CLIENT == constants.slot_car_update_client and constants.CAR_AND_RACE_UPDATE_CLIENT in constants.MQTT_CLIENT_SETTINGS:
            # Same client, combine into one
            return self.create_combined_client(constants.CAR_AND_RACE_UPDATE_CLIENT)

        if constants.CAR_AND_RACE_UPDATE_CLIENT in constants.MQTT_CLIENT_SETTINGS:
            self.car_and_race_update_client = self.create_client(
                "CarAndRaceMQTTClient",
                constants.CAR_AND_RACE_UPDATE_CLIENT,
                constants.CAR_AND_RACE_SUBSCRIPTION_TOPICS,
                self.callback_config_car_and_race
            )

        if constants.slot_car_update_client in constants.MQTT_CLIENT_SETTINGS:
            self.slot_car_update_client = self.create_client(
                "SlotCarMQTTClient",
                constants.slot_car_update_client,
                constants.SLOT_CARS_SUBSCRIPTION_TOPICS,
                self.callback_config_slot_cars
            )

    def create_combined_client(self, client_setting):
        combined_callback_config = {
            **self.callback_config_car_and_race,
            **self.callback_config_slot_cars
        }
        combined_topics = constants.CAR_AND_RACE_SUBSCRIPTION_TOPICS + \
            constants.SLOT_CARS_SUBSCRIPTION_TOPICS
        host, port = constants.CLIENT_TO_MQTT_HOSTS.get(client_setting)
        is_iot_core = client_setting == constants.CLIENT_OPTIONS["IOT_CORE"]
        client = mqtt_client.IoTCoreMqttClient if is_iot_core else mqtt_client.PahoMqttClient

        self.car_and_race_update_client = client(
            "MQTTClient", host, port, combined_topics, combined_callback_config
        )
        self.slot_car_update_client = self.car_and_race_update_client  # It's the same client

    def create_client(self, id, client, topics, callback_config):
        iot_core_client = client == constants.CLIENT_OPTIONS["IOT_CORE"]
        mqtt_client_option = mqtt_client.IoTCoreMqttClient if iot_core_client else mqtt_client.PahoMqttClient
        host, port = constants.CLIENT_TO_MQTT_HOSTS.get(client)
        return mqtt_client_option(
            id,
            host,
            port,
            topics,
            callback_config
        )
