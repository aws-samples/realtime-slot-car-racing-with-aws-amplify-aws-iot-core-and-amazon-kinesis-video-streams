import json
import ast

from utils.byte_helper import ByteHelper
import utils.constants as constants

from collections import deque

class RacerHelper:
    def __init__(self) -> None:
        self.current_race_id = constants.INITIAL_RACE_ID
        self.current_int_array = constants.INITIAL_INT_ARRAY
        self.current_race_state = None

        self.cars = [Car(number=index+1) for index in range(constants.TOTAL_NUMBER_OF_CARS)]
        self.max_throttle_on_track = 0    # Between 0 and 100

        self.previous_int_array = []

        self.port_current = 0
        self.track_power_status = 0

        self.lapTimes = deque()
        self.raceAnalyticsItems = deque()
        self.previousLapTime = None

    def handleRaceUpdate(self, json_string):
        try:
            json_object = json.loads(json_string)
        except ValueError as e:
            print("invalid json")
            return

        race_state = json_object.get("gameState")
        if race_state is None or race_state not in constants.RACE_STATES_SET:
            return

        if race_state == constants.RACE_STATE_LOBBY:
            self.initialiseRace(json_object)

        if race_state == constants.RACE_STATE_FORMATION_LAPS:
            self._handleFormationLapsSetting(json_object)

        if self.current_race_state in constants.RACE_DRIVING_STATES and race_state not in constants.RACE_DRIVING_STATES:
            self._reset_all_car_finish_times()

        self.current_race_state = race_state

        if race_state not in constants.RACE_DRIVING_STATES and race_state != constants.RACE_STATE_FORMATION_LAPS:
            self._updateCarPlayers(json_object)

        self.generateIntArray()

    def _updateCarPlayers(self, json_object):
        car_claims = json_object.get("carClaims")
        for car_claim in car_claims:
            self.cars[car_claim.get("carId")-1].playerId = car_claim.get("playerId", "")

    def _handleFormationLapsSetting(self, json_object):
        car_claims = json_object.get("carClaims")
        for car_claim in car_claims:
            carId = car_claim.get("carId")
            formationCar = constants.FORMATION_LAPS_CARS.get(carId)
            self.cars[carId-1].playerId = car_claim.get("playerId") if formationCar.get("enabled") else ""
            self.cars[carId-1].throttle = formationCar.get("throttle", 0)

    def handleCarUpdate(self, json_string):
        try:
            json_object = json.loads(json_string)
        except ValueError as e:
            print("invalid json")
            return

        if json_object.get("raceId") is None or json_object.get("raceId") != self.current_race_id:
            print("Race mismatch")
            return -1  # ERROR

        self.updateCar(json_object)
        self.generateIntArray()

    def handleNewLapTime(self, race_id, player_id, time_in_ms):
        new_lap_time = LapTime(race_id, player_id, time_in_ms)
        if self.previousLapTime and new_lap_time == self.previousLapTime:
            return
        self.lapTimes.append(new_lap_time)

    def initialiseRace(self, json_object):
        race_id = json_object.get("raceId")

        self.current_race_id = race_id
        self.cars = [Car(number=index+1) for index in range(constants.TOTAL_NUMBER_OF_CARS)]

        self.current_int_array = constants.INITIAL_INT_ARRAY
        self.current_race_state = constants.RACE_STATE_LOBBY

    def updateCar(self, data):
        car_id = int(data.get("carId"))-1
        for key, value in data.items():
            setattr(self.cars[car_id], key, value)


    def generateIntArray(self):
        array_of_ints = []
        # Set operation mode:
        array_of_ints.append(255)
        self.appendCarInts(array_of_ints)
        array_of_ints.append(ByteHelper.crc8(array_of_ints))
        self.current_int_array = array_of_ints

    def appendCarInts(self, array_of_ints):
        led_byte_helper = ByteHelper()
        for index, car in enumerate(self.cars):
            player = car.playerId
            if player is None or player == "":
                # This car is not claimed, so all 0s and the led light is off
                array_of_ints.append(255)
                continue

            byte_helper = ByteHelper()

            led_byte_helper.set_bit(index, 1)

            if car.brakesOnReq == True:
                byte_helper.set_bit(7, 1)

            if car.laneChangeReq == True:
                byte_helper.set_bit(6, 1)

            byte_helper.set_car_speed(
                self._getFinalCarSpeed(car.throttle))

            array_of_ints.append(byte_helper.get_int_ones_complement())
        game_timer_led_values = self._get_game_timer_status_led()
        led_byte_helper.set_bit(6, game_timer_led_values[1])
        led_byte_helper.set_bit(7, game_timer_led_values[0])

        array_of_ints.append(led_byte_helper.number)

    # Transform JSON bool ("true" / "false") to int (0, 1)
    def _jsonBoolToInt(self, json_bool):
        return 1 if json_bool == "true" else 0

    def _getMaxTrackSpeed(self):
        max_throttle_on_track = 0

        full_throttle_states = [
            constants.RACE_STATE_GREEN_FLAG,
            constants.RACE_STATE_PRACTICE
        ]
        if self.current_race_state in full_throttle_states:
            max_throttle_on_track = 100

        if self.current_race_state == constants.RACE_STATE_YELLOW_FLAG:
            max_throttle_on_track = constants.YELLOW_FLAG_MAX_SPEED

        return max_throttle_on_track

    def _get_game_timer_status_led(self):
        if self.current_race_state in constants.RACE_DRIVING_STATES:
            return [1, 0]
        return [1, 1]

    def _set_race_state(self, race_state):
        self.current_race_state = race_state

    def _getFinalCarSpeed(self, json_throttle):
        min_throttle = min(
            json_throttle,
            self._getMaxTrackSpeed(),
        )
        return constants.THROTTLE_SETTINGS.get(min_throttle, 0)

    def handleRaceTrackData(self, int_array_string):
        if self.current_race_state not in constants.RACE_DRIVING_STATES:
            return

        int_array = ast.literal_eval(int_array_string.decode('utf-8'))
        self.handleIntArray(int_array)

    def handleIntArray(self, int_array):
        first_int = int_array[0]
        self.track_power_status = first_int & 1 != 0

        # Ignoring Handset Values
        self.port_current = int_array[7]
        # Only look at the last 3 bits (111 = 7)
        car_id_past_sf_line = int_array[8] & 7

        if 0 < car_id_past_sf_line < 7:
            nr_of_bytes_making_up_game_ticks = 4
            game_time_ticks = 0
            for i in range(0, nr_of_bytes_making_up_game_ticks):
                game_time_ticks += int_array[9 + i] << 8 * i
            game_time_millisec = round(
                constants.GAMETICK_IN_MILLISECOND * game_time_ticks)
            print("CAR_ID_CROSSED_LINE: ", car_id_past_sf_line)
            self.handleCarLap(car_id_past_sf_line, game_time_millisec)

    def handleCarLap(self, car_id, game_time_in_ms):
        last_game_time = self.cars[car_id - 1].latestFinishLinePassTime
        lap_time = game_time_in_ms - last_game_time
        if lap_time > constants.MINIMUM_LAP_TIME_IN_MILLISECONDS:
            self.handleNewLapTime(self.current_race_id,
                                  self.cars[car_id-1].playerId, lap_time)

        self.cars[car_id - 1].latestFinishLinePassTime = game_time_in_ms

    def _reset_all_car_finish_times(self):
        for i in range(0, len(self.cars)):
            self.cars[i].latestFinishLinePassTime = 0


class LapTime:
    def __init__(self, race_id, player_id, lap_time_in_ms) -> None:
        self.race_id = race_id
        self.player_id = player_id
        self.lap_time_in_ms = lap_time_in_ms

    def json_representation_for_mqtt(self):
        return json.dumps({
            "raceId": self.race_id,
            "playerId": self.player_id,
            "timeInMilliSec": self.lap_time_in_ms
        })

    def __eq__(self, other_object: object) -> bool:
        return self.race_id == other_object.race_id \
            and self.player_id == other_object.player_id \
            and self.lap_time_in_ms == other_object.lap_time_in_ms

    def __repr__(self) -> str:
        return f"{self.race_id}:{self.player_id}:{self.lap_time_in_ms}"



class Car:
    def __init__(self, number, playerId="", throttle=0, laneChangeReq=False, brakesOnReq=False, latestFinishLinePassTime=0) -> None:
        self.number = number
        self.playerId = playerId
        self.throttle = throttle
        self.laneChangeReq = laneChangeReq
        self.brakesOnReq = brakesOnReq
        self.latestFinishLinePassTime = latestFinishLinePassTime

    def __eq__(self, __o: object) -> bool:
        return (
            self.number == __o.number \
            and self.playerId == __o.playerId \
            and self.throttle == __o.throttle \
            and self.laneChangeReq == __o.laneChangeReq \
            and self.brakesOnReq == __o.brakesOnReq \
            and self.latestFinishLinePassTime == __o.latestFinishLinePassTime \
        )