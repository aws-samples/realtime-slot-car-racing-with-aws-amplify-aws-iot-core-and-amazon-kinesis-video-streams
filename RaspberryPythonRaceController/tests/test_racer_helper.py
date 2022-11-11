import unittest
import json
import copy

from utils.racer_helper import RacerHelper, LapTime, Car
from parameterized import parameterized

import utils.constants as constants
from utils.byte_helper import ByteArrayHelper

RACE_ID = "e78ad5ea-d512-4c68-838a-631f5b7f1518"
PLAYER_1_ID = "86ebf1bb-417f-4f1c-82bd-d0257bd9986b"
PLAYER_2_ID = "d4f039b5-db34-4615-8333-b5c4c6118653"
PLAYER_3_ID = ""
PLAYER_4_ID = ""
PLAYER_5_ID = ""
PLAYER_6_ID = ""

PLAYER_IDS = [PLAYER_1_ID, PLAYER_2_ID, PLAYER_3_ID,
              PLAYER_4_ID, PLAYER_5_ID, PLAYER_6_ID]


class RaceHelperTest(unittest.TestCase):
    base_game_state_update_object = {
        "raceId": RACE_ID,
        "gameState": constants.RACE_STATE_LOBBY,
        "carClaims": [
            {"carId": 1, "playerId": PLAYER_1_ID},
            {"carId": 2, "playerId": PLAYER_2_ID},
            {"carId": 3, "playerId": PLAYER_3_ID},
            {"carId": 4, "playerId": PLAYER_4_ID},
            {"carId": 5, "playerId": PLAYER_5_ID},
            {"carId": 6, "playerId": PLAYER_6_ID}
        ]
    }

    base_expected_cars = [
        Car(
            number=1,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
        Car(
            number=2,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
        Car(
            number=3,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
        Car(
            number=4,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
        Car(
            number=5,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
        Car(
            number=6,
            playerId="",
            throttle=0,
            laneChangeReq=0,
            brakesOnReq=0,
            latestFinishLinePassTime=0
        ),
    ]

    base_expected_deconstructed_sending_object = {
        'operation_mode': "b'\\xff'",
        'led_status': "b'\\x80'",
        'checksum': "b'\\x90'",
        'drive_packets': {
            'car_2': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'car_1': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'car_3': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'car_4': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'car_5': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'car_6': {'binary_string': '0b00000000', 'brakesOnReq': False, 'laneChangeReq': False, 'power': 0}
        }
    }

    def setUp(self):
        self.raceHelper = RacerHelper()
        input_json_string = json.dumps(self.base_game_state_update_object)
        self.raceHelper.handleRaceUpdate(input_json_string)

    def test_empty_init_values(self):
        RaceHelperObject = RacerHelper()

        expected_current_race_id = constants.INITIAL_RACE_ID
        expected_cars = self.base_expected_cars

        expected_max_speed_on_track = 0    # Between 0 and 100

        self.assertEqual(RaceHelperObject.current_race_id,
                         expected_current_race_id)
        self.assertEqual(RaceHelperObject.cars, expected_cars)
        self.assertEqual(RaceHelperObject._getMaxTrackSpeed(),
                         expected_max_speed_on_track)

    def test_initialise_race(self):
        raceHelperObject = RacerHelper()
        input_json_string = json.dumps({
            "raceId": RACE_ID,
            "gameState": constants.RACE_STATE_LOBBY,
            "carClaims": [
                {"carId": 1, "playerId": ""},
                {"carId": 2, "playerId": ""},
                {"carId": 3, "playerId": ""},
                {"carId": 4, "playerId": ""},
                {"carId": 5, "playerId": ""},
                {"carId": 6, "playerId": ""}
            ]
        })

        raceHelperObject.handleRaceUpdate(input_json_string)

        expected_current_race_id = RACE_ID
        expected_max_speed_on_track = 0    # Between 0 and 100

        self.assertEqual(raceHelperObject.current_race_id,
                         expected_current_race_id)
        self.assertEqual(raceHelperObject.cars, self.base_expected_cars)
        self.assertEqual(raceHelperObject._getMaxTrackSpeed(),
                         expected_max_speed_on_track)
        self.assertEqual(raceHelperObject.current_race_state,
                         constants.RACE_STATE_LOBBY)

    def test_race_after_practice_initiated(self):
        input_json_string = json.dumps({
            "raceId": RACE_ID,
            "gameState": constants.RACE_STATE_PRACTICE,
            "carClaims": [
                {"carId": 1, "playerId": PLAYER_1_ID},
                {"carId": 2, "playerId": PLAYER_2_ID},
                {"carId": 3, "playerId": PLAYER_3_ID},
                {"carId": 4, "playerId": PLAYER_4_ID},
                {"carId": 5, "playerId": PLAYER_5_ID},
                {"carId": 6, "playerId": PLAYER_6_ID}
            ]
        })

        self.raceHelper.handleRaceUpdate(input_json_string)

        expected_cars_array = self.base_expected_cars.copy()
        for index, expected_car in enumerate(expected_cars_array):
            expected_car.playerId = PLAYER_IDS[index]

        expected_current_race_id = RACE_ID
        expected_max_speed_on_track = 100

        self.assertEqual(self.raceHelper.current_race_id,
                         expected_current_race_id)
        self.assertEqual(self.raceHelper.cars, expected_cars_array)
        self.assertEqual(self.raceHelper._getMaxTrackSpeed(),
                         expected_max_speed_on_track)
        self.assertEqual(self.raceHelper.current_race_state,
                         constants.RACE_STATE_PRACTICE)

    def test_empty_race_byte_array(self):
        raceHelper = RacerHelper()
        raceHelper.generateIntArray()

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                'car_1': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 192,
            'checksum': 106
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            raceHelper.current_int_array)
        self.assertEqual(actual_object, expected_object)

    def test_initial_generate_byte_array(self):
        # Race helper with a couple of cars - not started
        self.raceHelper.generateIntArray()
        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                'car_1': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 195,
            'checksum': 99
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            self.raceHelper.current_int_array
        )
        self.assertEqual(actual_object, expected_object)

    def test_race_in_lobby_car_1_with_throttle_still_returns_0_speed_in_array(self):
        THROTTLE = 50
        car_update_object = json.dumps({
            "raceId": RACE_ID,
            "carId": 1,
            "playerId": PLAYER_1_ID,
            "throttle": THROTTLE,
            "laneChangeReq": False,
            "brakesOnReq": False
        })
        self.raceHelper.handleCarUpdate(car_update_object)

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                # STILL 0 POWER
                'car_1': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 195,
            'checksum': 99
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            self.raceHelper.current_int_array
        )
        self.assertEqual(actual_object, expected_object)

    def test_race_green_car_1_throttle_50_settings_returns_proper_array(self):
        self.raceHelper._set_race_state(constants.RACE_STATE_GREEN_FLAG)
        THROTTLE = 50
        car_update_object = json.dumps({
            "raceId": RACE_ID,
            "carId": 1,
            "playerId": PLAYER_1_ID,
            "throttle": THROTTLE,
            "laneChangeReq": False,
            "brakesOnReq": False
        })
        self.raceHelper.handleCarUpdate(car_update_object)

        binary_string = format(constants.THROTTLE_SETTINGS[THROTTLE], '#010b')
        power_value = constants.THROTTLE_SETTINGS[THROTTLE]

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                # STILL 0 POWER
                'car_1': {'binary_string': binary_string, 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': power_value},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 131,
            'checksum': 130
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            self.raceHelper.current_int_array
        )
        self.assertEqual(actual_object, expected_object)

    @parameterized.expand([
        (0, ),
        (10, ),
        (20, ),
        (30, ),
        (40, ),
        (50, ),
        (60, ),
        (70, ),
        (80, ),
        (90, ),
        (100, ),
    ])
    def test_race_green_car_1_throttle_settings_returns_proper_array(self, throttle):
        self.raceHelper._set_race_state(constants.RACE_STATE_GREEN_FLAG)

        car_update_object = json.dumps({
            "raceId": RACE_ID,
            "carId": 1,
            "playerId": PLAYER_1_ID,
            "throttle": throttle,
            "laneChangeReq": False,
            "brakesOnReq": False
        })
        self.raceHelper.handleCarUpdate(car_update_object)

        binary_string = format(constants.THROTTLE_SETTINGS[throttle], '#010b')
        power_value = constants.THROTTLE_SETTINGS[throttle]

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                # STILL 0 POWER
                'car_1': {'binary_string': binary_string, 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': power_value},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 131,
            'checksum': 255
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            self.raceHelper.current_int_array
        )

        actual_object["checksum"] = 255  # OVERRIDE CHECKSUM AS WE DON'T CARE

        self.assertEqual(actual_object, expected_object)

    def test_car_2_throttle_60_switch_lane_and_brake_returns_proper_array(self):
        game_state_update_object = copy.deepcopy(
            self.base_game_state_update_object)
        game_state_update_object["gameState"] = constants.RACE_STATE_GREEN_FLAG
        self.raceHelper.handleRaceUpdate(json.dumps(game_state_update_object))

        THROTTLE = 60
        car_update_object = json.dumps({
            "raceId": RACE_ID,
            "carId": 2,
            "playerId": PLAYER_2_ID,
            "throttle": THROTTLE,
            "laneChangeReq": True,
            "brakesOnReq": True
        })
        self.raceHelper.handleCarUpdate(car_update_object)
        # 192 means first 2 bits set
        binary_string = format(
            192 ^ constants.THROTTLE_SETTINGS[THROTTLE], '#010b')
        power_value = constants.THROTTLE_SETTINGS[THROTTLE]

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                # STILL 0 POWER
                'car_1': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_2': {'binary_string': binary_string, 'brakesOnReqsOnReq': True, 'laneChangeReq': True, 'power': power_value},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 131,
            'checksum': 174
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            self.raceHelper.current_int_array
        )
        self.assertEqual(actual_object, expected_object)

    def test_slot_cars_int_array_no_race_data(self):
        test_int_array = ByteArrayHelper.generate_slot_cars_int_array_for_testing()

        expected_object = {
            'handset_track_status': {
                'handset_6': True,
                'handset_5': True,
                'handset_4': True,
                'handset_3': True,
                'handset_2': True,
                'handset_1': True,
                'track_power_status': True,
                'bit_7_should_be_true': True
            },
            'handset_1': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_2': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_3': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_4': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_5': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_6': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'aux_port_current': 24,
            'car_id_track': {
                'constant_bits_should_be_248': 248,
                'car_id': 'game_timer'
            },
            'game_timer_in_micro_seconds': 0,
            'slot_cars_buttons_should_be_0': 0,
            'checksum': 108
        }

        actual_object = ByteArrayHelper.race_track_array_of_ints_to_object(
            test_int_array
        )

        self.assertEqual(actual_object, expected_object)

    def test_slot_cars_int_array_no_race_data(self):
        test_int_array = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            encode_to_byte_array=False)

        expected_object = {
            'handset_track_status': {
                'handset_6': True,
                'handset_5': True,
                'handset_4': True,
                'handset_3': True,
                'handset_2': True,
                'handset_1': True,
                'track_power_status': True,
                'bit_7_should_be_true': True
            },
            'handset_1': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_2': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_3': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_4': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_5': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'handset_6': {'brakesOnReq': False, 'laneChangeReq': False, 'power': 0},
            'aux_port_current': 24,
            'car_id_track': {
                'constant_bits_should_be_248': 248,
                'car_id': 'game_timer'
            },
            'game_timer_in_micro_seconds': 0,
            'slot_cars_buttons_should_be_0': 0,
            'checksum': 108
        }

        actual_object = ByteArrayHelper.race_track_array_of_ints_to_object(
            test_int_array
        )

        self.assertEqual(actual_object, expected_object)


class LapTimeTest(unittest.TestCase):
    base_game_state_update_object = {
        "raceId": RACE_ID,
        "gameState": constants.RACE_STATE_GREEN_FLAG,
        "carClaims": [
            {"carId": 1, "playerId": PLAYER_1_ID},
            {"carId": 2, "playerId": PLAYER_2_ID},
            {"carId": 3, "playerId": PLAYER_3_ID},
            {"carId": 4, "playerId": PLAYER_4_ID},
            {"carId": 5, "playerId": PLAYER_5_ID},
            {"carId": 6, "playerId": PLAYER_6_ID}
        ]
    }

    def setUp(self):
        self.raceHelper = RacerHelper()
        update_object = copy.deepcopy(self.base_game_state_update_object)
        update_object["gameState"] = constants.RACE_STATE_LOBBY

        # INITIALISE RACE
        self.raceHelper.handleRaceUpdate(json.dumps(update_object))

        # SET RACE TO PRACTICE TO INITIALISE CLAIMS
        update_object["gameState"] = constants.RACE_STATE_PRACTICE
        self.raceHelper.handleRaceUpdate(json.dumps(update_object))

        # SET RACE TO GREEN_LIGHT TO ALLOW LAP TIMES
        update_object["gameState"] = constants.RACE_STATE_GREEN_FLAG
        self.raceHelper.handleRaceUpdate(json.dumps(update_object))

    def test_simple_new_lap_time_car_1(self):
        GAME_TIME_IN_MS = 12345
        CAR_ID = 1
        test_int_array = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID,
            game_time_in_ms=GAME_TIME_IN_MS
        )

        self.raceHelper.handleRaceTrackData(test_int_array)
        expected_lap_time = LapTime(RACE_ID, PLAYER_1_ID, GAME_TIME_IN_MS - 0)

        self.assertEqual(len(self.raceHelper.lapTimes), 1)
        self.assertEqual(self.raceHelper.lapTimes[0], expected_lap_time)

    def test_duplicate_lap_time_only_creates_one_item(self):
        GAME_TIME_IN_MS = 12345
        CAR_ID = 1
        test_int_array = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID,
            game_time_in_ms=GAME_TIME_IN_MS
        )

        expected_lap_time = LapTime(RACE_ID, PLAYER_1_ID, GAME_TIME_IN_MS - 0)

        # HANDLE FIRST TIME
        self.raceHelper.handleRaceTrackData(test_int_array)
        self.assertEqual(len(self.raceHelper.lapTimes), 1)
        self.assertEqual(self.raceHelper.lapTimes[0], expected_lap_time)

        # HANDLE SECOND TIME
        self.raceHelper.handleRaceTrackData(test_int_array)
        # <== still only one item in queue
        self.assertEqual(len(self.raceHelper.lapTimes), 1)
        self.assertEqual(self.raceHelper.lapTimes[0], expected_lap_time)

    def test_same_car_new_laptime_creates_2_objects(self):
        GAME_TIME_IN_MS = 12345
        DIFFERENCE_BETWEEN_LAPS = constants.MINIMUM_LAP_TIME_IN_MILLISECONDS + 1
        CAR_ID = 1

        LAP_TIME_1 = GAME_TIME_IN_MS
        LAP_TIME_2 = GAME_TIME_IN_MS + DIFFERENCE_BETWEEN_LAPS

        test_int_array_1 = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID, game_time_in_ms=LAP_TIME_1)
        test_int_array_2 = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID, game_time_in_ms=LAP_TIME_2)

        expected_lap_time_1 = LapTime(RACE_ID, PLAYER_1_ID, LAP_TIME_1 - 0)
        expected_lap_time_2 = LapTime(
            RACE_ID, PLAYER_1_ID, LAP_TIME_2 - LAP_TIME_1)

        # HANDLE FIRST TIME
        self.raceHelper.handleRaceTrackData(test_int_array_1)
        self.assertEqual(len(self.raceHelper.lapTimes), 1)
        self.assertEqual(self.raceHelper.lapTimes[0], expected_lap_time_1)

        # HANDLE SECOND TIME
        self.raceHelper.handleRaceTrackData(test_int_array_2)
        self.assertEqual(len(self.raceHelper.lapTimes), 2)
        self.assertEqual(self.raceHelper.lapTimes[1], expected_lap_time_2)

    def test_two_cars_passing_start_finish_line_closely_after_another_creates_2_objects(self):
        GAME_TIME_IN_MS = 12345
        DIFFERENCE_BETWEEN_LAPS = 10
        CAR_ID_1 = 1
        CAR_ID_2 = 2

        LAP_TIME_1 = GAME_TIME_IN_MS
        LAP_TIME_2 = GAME_TIME_IN_MS + DIFFERENCE_BETWEEN_LAPS

        test_int_array_1 = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID_1,
            game_time_in_ms=LAP_TIME_1
        )
        test_int_array_2 = ByteArrayHelper.generate_slot_cars_int_array_for_testing(
            car_id=CAR_ID_2,
            game_time_in_ms=LAP_TIME_2
        )

        expected_lap_time_1 = LapTime(RACE_ID, PLAYER_1_ID, LAP_TIME_1 - 0)
        expected_lap_time_2 = LapTime(RACE_ID, PLAYER_2_ID, LAP_TIME_2 - 0)

        # HANDLE FIRST TIME
        self.raceHelper.handleRaceTrackData(test_int_array_1)
        self.assertEqual(len(self.raceHelper.lapTimes), 1)
        self.assertEqual(self.raceHelper.lapTimes[0], expected_lap_time_1)

        # HANDLE SECOND TIME
        self.raceHelper.handleRaceTrackData(test_int_array_2)
        self.assertEqual(len(self.raceHelper.lapTimes), 2)
        self.assertEqual(self.raceHelper.lapTimes[1], expected_lap_time_2)

    def test_formation_lap_time_init_race_not_started_yet_all_cars_stopped_correct_leds_on(self):
        raceHelper = RacerHelper()
        update_object = copy.deepcopy(self.base_game_state_update_object)

        # INITIALISE RACE
        update_object["gameState"] = constants.RACE_STATE_LOBBY
        raceHelper.handleRaceUpdate(json.dumps(update_object))

        # SET RACE TO FORMATION TO INITIALISE CLAIMS
        update_object["gameState"] = constants.RACE_STATE_FORMATION_LAPS
        raceHelper.handleRaceUpdate(json.dumps(update_object))

        # Check exppected values
        raceHelper.generateIntArray()
        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                'car_1': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_2': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            'led_status': 195,  # 11000011 Green + Red on + First two cars light on
            'checksum': 99
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            raceHelper.current_int_array
        )

        self.assertEqual(actual_object, expected_object)

    def test_formation_lap_time_started_race_correct_values_set(self):
        raceHelper = RacerHelper()
        update_object = copy.deepcopy(self.base_game_state_update_object)

        # INITIALISE RACE
        update_object["gameState"] = constants.RACE_STATE_LOBBY
        raceHelper.handleRaceUpdate(json.dumps(update_object))

        # SET RACE TO FORMATION TO INITIALISE CLAIMS
        update_object["gameState"] = constants.RACE_STATE_FORMATION_LAPS
        raceHelper.handleRaceUpdate(json.dumps(update_object))

        # SET RACE TO GREEN LIGHT TO CHECK THROTTLE
        update_object["gameState"] = constants.RACE_STATE_GREEN_FLAG
        raceHelper.handleRaceUpdate(json.dumps(update_object))

        expected_power_car = constants.THROTTLE_SETTINGS[constants.FORMATION_LAP_THROTTLE]

        expected_object = {
            'operation_mode': 255,
            'drive_packets': {
                # Throttle 20
                'car_1': {'binary_string': '0b00001011', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': expected_power_car},
                'car_2': {'binary_string': '0b00001011', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': expected_power_car},
                'car_3': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_4': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_5': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0},
                'car_6': {'binary_string': '0b00000000', 'brakesOnReqsOnReq': False, 'laneChangeReq': False, 'power': 0}
            },
            # 10000011 Green on + Red off (race started), First two cars light on
            'led_status': 131,
            'checksum': 28
        }

        actual_object = ByteArrayHelper.sending_array_of_ints_to_object(
            raceHelper.current_int_array
        )

        self.assertEqual(actual_object, expected_object)
