import json

from utils.racer_helper import RacerHelper
from utils.clients_setup_helper import ClientsSetupHelper

import utils.constants as constants

from time import sleep

import datetime


class RaceRunner:
    def __init__(self) -> None:
        self.racerHelper = RacerHelper()
        clients_helper = ClientsSetupHelper(self.racerHelper)
        self.car_and_race_update_client = clients_helper.car_and_race_update_client
        self.race_track_update_client = clients_helper.slot_car_update_client

    def send_lap_times_to_iot_core(self):
        while len(self.racerHelper.lapTimes) > 0:
            lap_time = self.racerHelper.lapTimes.popleft()
            self.car_and_race_update_client.send_payload(
                payload={
                    "topic": constants.LAP_TIME_TOPIC,
                    "message_string": lap_time.json_representation_for_mqtt()
                }
            )

    def send_race_analytics_to_mqtt(self):
        analytics_items = []
        while len(self.racerHelper.raceAnalyticsItems) > 0:
            driveIntArray, slotcarIntArray = self.racerHelper.raceAnalyticsItems.popleft()
            analytics_items.append({
                "raceId": self.racerHelper.current_race_id,
                "driveIntArray": str(driveIntArray),
                "slotcarIntArray": str(slotcarIntArray),
                "timestamp": datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')
            })

        if len(analytics_items) > 0:
            self.car_and_race_update_client.send_payload(
                payload={
                    "topic": constants.RACE_ANALYTICS_TOPIC,
                    "message_string": json.dumps(analytics_items)
                }
            )

    def send_int_array_to_slot_cars(self):
        if self.race_track_update_client._client_type in constants.DIRECT_SLOT_CAR_CLIENTS:
            # If we're talking directly to the slot cars, repeatedly send the byte array
            payload = {
                "int_array": self.racerHelper.current_int_array,
                "recv_handler": self.racerHelper.handleIntArray
            }
            self.race_track_update_client.send_payload(payload=payload, racer_helper=self.racerHelper)

        elif self.race_track_update_client._client_type in constants.MQTT_CLIENT_SETTINGS:
            # If we're not talking directly only send byte array if we have a new array
            if self.racerHelper.previous_int_array != self.racerHelper.current_int_array:
                print(self.racerHelper.current_int_array)
                payload = {
                    "topic": constants.TRACK_MQTT_TOPIC_NAME_PUB,
                    "message_string": str(self.racerHelper.current_int_array)
                }
                self.race_track_update_client.send_payload(payload=payload)
                self.racerHelper.previous_int_array = self.racerHelper.current_int_array
        else:
            raise ValueError("Unrecognised Client")

    def is_connected(self):
        return self.car_and_race_update_client._connected == True and self.race_track_update_client._connected == True

    def run_race(self):
        last_run_time_slot_cars, last_run_time_iot_core, last_run_time_analytics = datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()
        while True:
            if not self.is_connected():
                print("waiting for connection...")
                sleep(1)
                continue

            current_run_time = datetime.datetime.now()

            # TODO: REFACTOR THIS CODE
            time_elapsed_slot_cars = (current_run_time - last_run_time_slot_cars).total_seconds() * 1000 # Elapsed time in MS
            if time_elapsed_slot_cars > constants.SLOT_CARS_SERIAL_REFRESH_RATE_MILLISECONDS:
                self.send_int_array_to_slot_cars()
                last_run_time_slot_cars = current_run_time

            time_elapsed_iot_core = (current_run_time - last_run_time_iot_core).total_seconds() * 1000 # Elapsed time in MS
            if time_elapsed_iot_core > constants.MQTT_REFRESH_RATE_MILLISECONDS:
                self.send_lap_times_to_iot_core()
                last_run_time_iot_core = current_run_time

            time_elapsed_iot_core = (current_run_time - last_run_time_analytics).total_seconds() * 1000 # Elapsed time in MS
            if constants.SEND_RACE_ANALYTICS_TO_MQTT and time_elapsed_iot_core > constants.ANALYTICS_REFRESH_RATE_MILLISECONDS:
                self.send_race_analytics_to_mqtt()
                last_run_time_analytics = current_run_time

            sleep(0.01) # Wait 10 ms anyways


if __name__ == "__main__":
    RaceRunner().run_race()
