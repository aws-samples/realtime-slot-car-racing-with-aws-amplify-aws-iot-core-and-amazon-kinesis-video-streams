CLIENT_OPTIONS = {
    "IOT_CORE": 'iot_core',
    "LOCAL_MQTT": "local_mqtt",
    "REMOTE_MQTT": "remote_mqtt",
    "SERIAL": "serial",
    "USB": "usb"
}

CLIENT_OPTIONS_ENUM = {
    1: CLIENT_OPTIONS["IOT_CORE"],
    2: CLIENT_OPTIONS["LOCAL_MQTT"],
    3: CLIENT_OPTIONS["REMOTE_MQTT"],
    4: CLIENT_OPTIONS["SERIAL"],
    5: CLIENT_OPTIONS["USB"]
}

####
# EDIT THE LINES BELOW TO UPDATE WHICH ENDPOINTS TO USE. SEE OPTIONS ABOVE
# 1 = IOT_CORE, 2 = LOCAL_MQTT, 3 = REMOTE_MQTT (test.mosquitto.org)
CAR_AND_RACE_CLIENT_SELECTION = 1
SLOT_CARS_CLIENT_SELECTION = 3

MQTT_CLIENT_SETTINGS = [
    CLIENT_OPTIONS["REMOTE_MQTT"],
    CLIENT_OPTIONS["LOCAL_MQTT"],
    CLIENT_OPTIONS["IOT_CORE"]
]

DIRECT_SLOT_CAR_CLIENTS = [
    CLIENT_OPTIONS["SERIAL"],
    CLIENT_OPTIONS["USB"],
]

LOCAL_MQTT_ENDPOINT_HOST = "127.0.0.1"
LOCAL_MQTT_ENDPOINT_PORT = 1883

AWS_IOT_CORE_HOST = "ah9frbb7pxug4-ats.iot.us-west-1.amazonaws.com"
AWS_IOT_CORE_PORT = 8883

MOSQUITTO_TEST_MQTT_ENDPOINT_HOST = "test.mosquitto.org"
MOSQUITTO_TEST_ENDPOINT_PORT = 1883

FORMATION_LAP_THROTTLE = 20

FORMATION_LAPS_CARS = {
    1: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
    2: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
    3: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
    4: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
    5: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
    6: {"enabled": True, "throttle": FORMATION_LAP_THROTTLE},
}
####

CAR_AND_RACE_UPDATE_CLIENT = CLIENT_OPTIONS_ENUM[CAR_AND_RACE_CLIENT_SELECTION]
slot_car_update_client = CLIENT_OPTIONS_ENUM[SLOT_CARS_CLIENT_SELECTION]

MQTT_REFRESH_RATE_MILLISECONDS = 100
SLOT_CARS_SERIAL_REFRESH_RATE_MILLISECONDS = 100
ANALYTICS_REFRESH_RATE_MILLISECONDS = 1000

INITIAL_RACE_ID = "1bb42be6-24cb-41ac-b1d8-955e7bc2f510"

SEND_RACE_ANALYTICS_TO_MQTT = True

TOTAL_NUMBER_OF_CARS = 6
YELLOW_FLAG_MAX_SPEED = 10
RED_FLAG_MAX_SPEED = 0
JSON_TRUE_VALUE = "true"
JSON_FALSE_VALUE = "false"

TALK_TO_TRACK_OVER_MQTT = False
TRACK_MQTT_TOPIC_NAME_PUB = "6cpb/outgoing"
TRACK_MQTT_TOPIC_NAME_SUB = "6cpb/incoming"

GAME_STATE_UPDATE_TOPIC = 'GAME_STATE_UPDATE'
CAR_CONTROL_UPDATE_TOPIC = 'CAR_CONTROL_UPDATE'
LAP_TIME_TOPIC = "RACE_LAP_TIME"
RACE_ANALYTICS_TOPIC = "RACE_ANALYTICS"

CLIENT_TO_MQTT_HOSTS = {
    CLIENT_OPTIONS["IOT_CORE"]: [AWS_IOT_CORE_HOST, AWS_IOT_CORE_PORT],
    CLIENT_OPTIONS["LOCAL_MQTT"]: [LOCAL_MQTT_ENDPOINT_HOST, LOCAL_MQTT_ENDPOINT_PORT],
    CLIENT_OPTIONS["REMOTE_MQTT"]: [MOSQUITTO_TEST_MQTT_ENDPOINT_HOST, MOSQUITTO_TEST_ENDPOINT_PORT],
}

CAR_AND_RACE_SUBSCRIPTION_TOPICS = [
    GAME_STATE_UPDATE_TOPIC, CAR_CONTROL_UPDATE_TOPIC]
SLOT_CARS_SUBSCRIPTION_TOPICS = [TRACK_MQTT_TOPIC_NAME_SUB]

GAME_TICK_MICROSECONDS = 6.4
GAMETICK_IN_MILLISECOND = GAME_TICK_MICROSECONDS / 1000  # 6.4 microsecond
MINIMUM_LAP_TIME_IN_MILLISECONDS = 1500

INITIAL_INT_ARRAY = [255, 255, 255, 255, 255, 255, 255, 0, 36]

THROTTLE_SETTINGS = {
    0: 0,
    10: 10,
    20: 11,
    30: 12,
    40: 13,
    50: 14,
    60: 15,
    70: 16,
    80: 17,
    90: 18,
    100: 19,
}

RACE_STATE_LOBBY = "lobby"
RACE_STATE_PRACTICE = "practice"
RACE_STATE_PENDING = "pending"
RACE_STATE_RED_FLAG = "red_flag"
RACE_STATE_YELLOW_FLAG = "yellow_flag"
RACE_STATE_GREEN_FLAG = "green_flag"
RACE_STATE_CHECKERED_FLAG = "checkered_flag"
RACE_STATE_ABORTED = "aborted"
RACE_STATE_FORMATION_LAPS = "formation_laps"

RACE_STATES_SET = set([
    RACE_STATE_LOBBY,
    RACE_STATE_PRACTICE,
    RACE_STATE_PENDING,
    RACE_STATE_RED_FLAG,
    RACE_STATE_YELLOW_FLAG,
    RACE_STATE_GREEN_FLAG,
    RACE_STATE_CHECKERED_FLAG,
    RACE_STATE_ABORTED,
    RACE_STATE_FORMATION_LAPS
])

RACE_DRIVING_STATES = [
    RACE_STATE_PRACTICE,
    RACE_STATE_YELLOW_FLAG,
    RACE_STATE_GREEN_FLAG,
]
