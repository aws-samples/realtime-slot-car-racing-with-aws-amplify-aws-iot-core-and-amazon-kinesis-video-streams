from utils.constants import TOTAL_NUMBER_OF_CARS, GAMETICK_IN_MILLISECOND

class ByteHelper:
    def __init__(self) -> None:
        self.number = 0

    def set_number(self, int_value):
        self.number = int_value

    def set_number_from_byte(self, byte_value):
        self.number = int.from_bytes(byte_value, 'little')

    def get_bit(self, index):
        return ((self.number >> index & 1) != 0)

    def set_bit(self, index, bit_value):
        if bit_value == 1:
            self.number = self.number | (1 << index)
        elif bit_value == 0:
            self.number = self.number & ~(1 << index)
        else:
            raise ValueError("Invalid value, must be 0 or 1")

    def set_car_speed(self, value):
        # Car speed is represented by setting first 5 bits to value 0 -> 63 in one's complement
        if value > 63: # Doesn't fit in 4 bits
            return
        self.number = self.number ^ value

    def get_byte(self):
        return self.number.to_bytes(1, 'little')

    def get_int_ones_complement(self):
        return self.number ^ 0xFF

    @staticmethod
    def crc8(msg):
        CRC8_LOOK_UP_TABLE = [
            0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15, 0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
            0x70, 0x77, 0x7E, 0x79, 0x6C, 0x6B, 0x62, 0x65, 0x48, 0x4F, 0x46, 0x41, 0x54, 0x53, 0x5A, 0x5D,
            0xE0, 0xE7, 0xEE, 0xE9, 0xFC, 0xFB, 0xF2, 0xF5, 0xD8, 0xDF, 0xD6, 0xD1, 0xC4, 0xC3, 0xCA, 0xCD,
            0x90, 0x97, 0x9E, 0x99, 0x8C, 0x8B, 0x82, 0x85, 0xA8, 0xAF, 0xA6, 0xA1, 0xB4, 0xB3, 0xBA, 0xBD,
            0xC7, 0xC0, 0xC9, 0xCE, 0xDB, 0xDC, 0xD5, 0xD2, 0xFF, 0xF8, 0xF1, 0xF6, 0xE3, 0xE4, 0xED, 0xEA,
            0xB7, 0xB0, 0xB9, 0xBE, 0xAB, 0xAC, 0xA5, 0xA2, 0x8F, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9D, 0x9A,
            0x27, 0x20, 0x29, 0x2E, 0x3B, 0x3C, 0x35, 0x32, 0x1F, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0D, 0x0A,
            0x57, 0x50, 0x59, 0x5E, 0x4B, 0x4C, 0x45, 0x42, 0x6F, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7D, 0x7A,
            0x89, 0x8E, 0x87, 0x80, 0x95, 0x92, 0x9B, 0x9C, 0xB1, 0xB6, 0xBF, 0xB8, 0xAD, 0xAA, 0xA3, 0xA4,
            0xF9, 0xFE, 0xF7, 0xF0, 0xE5, 0xE2, 0xEB, 0xEC, 0xC1, 0xC6, 0xCF, 0xC8, 0xDD, 0xDA, 0xD3, 0xD4,
            0x69, 0x6E, 0x67, 0x60, 0x75, 0x72, 0x7B, 0x7C, 0x51, 0x56, 0x5F, 0x58, 0x4D, 0x4A, 0x43, 0x44,
            0x19, 0x1E, 0x17, 0x10, 0x05, 0x02, 0x0B, 0x0C, 0x21, 0x26, 0x2F, 0x28, 0x3D, 0x3A, 0x33, 0x34,
            0x4E, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5C, 0x5B, 0x76, 0x71, 0x78, 0x7F, 0x6A, 0x6D, 0x64, 0x63,
            0x3E, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2C, 0x2B, 0x06, 0x01, 0x08, 0x0F, 0x1A, 0x1D, 0x14, 0x13,
            0xAE, 0xA9, 0xA0, 0xA7, 0xB2, 0xB5, 0xBC, 0xBB, 0x96, 0x91, 0x98, 0x9F, 0x8A, 0x8D, 0x84, 0x83,
            0xDE, 0xD9, 0xD0, 0xD7, 0xC2, 0xC5, 0xCC, 0xCB, 0xE6, 0xE1, 0xE8, 0xEF, 0xFA, 0xFD, 0xF4, 0xF3
        ]
        crc6Rx = CRC8_LOOK_UP_TABLE[msg[0]]
        for i in range(1, 8):
            crc6Rx = CRC8_LOOK_UP_TABLE[crc6Rx ^ msg[i]]
        return crc6Rx

class ByteArrayHelper:
    def sending_array_of_ints_to_object(int_array):
        object_to_return = {}

        object_to_return["operation_mode"] = int_array[0]
        drive_packets = {}
        for i in range(1, 7):
            # Reverse ones complement
            car_int = int_array[i] ^ 0xFF
            # Take 1st -> 6th bit for speed
            car_speed = car_int & ~(1 << 7)
            car_speed = car_speed & ~(1 << 6)

            drive_packets[f"car_{i}"] = {
                "binary_string": format(car_int, '#010b'),
                "brakesOnReqsOnReq": car_int & 128 != 0,  # Check 8th bit
                "laneChangeReq": car_int & 64 != 0,  # Check 7th bit
                "power": car_speed
            }
        object_to_return["drive_packets"] = drive_packets
        object_to_return["led_status"] = int_array[7]
        object_to_return["checksum"] = int_array[8]
        return object_to_return

    def race_track_array_of_ints_to_object(int_array):
        object_to_return = {}
        byte_helper = ByteHelper()
        byte_helper.set_number(int_array[0])

        object_to_return["handset_track_status"] = {
            "handset_6": byte_helper.get_bit(6),
            "handset_5": byte_helper.get_bit(5),
            "handset_4": byte_helper.get_bit(4),
            "handset_3": byte_helper.get_bit(3),
            "handset_2": byte_helper.get_bit(2),
            "handset_1": byte_helper.get_bit(1),
            "track_power_status": byte_helper.get_bit(0),
            "bit_7_should_be_true": byte_helper.get_bit(7)
        }

        for i in range(TOTAL_NUMBER_OF_CARS):
            car_int = int_array[1 + i] ^ 0xFF

            # Take 1st -> 6th bit for speed
            car_speed = car_int & ~(1 << 7)
            car_speed = car_speed & ~(1 << 6)
            object_to_return[f"handset_{i + 1}"] = {
                "brakesOnReq": car_int & 128 != 0,
                "laneChangeReq": car_int & 64 != 0,
                "power": car_speed
            }

        object_to_return["aux_port_current"] = int_array[7]
        car_id_lookup = {
            0: "game_timer",
            1: "car_1",
            2: "car_2",
            3: "car_3",
            4: "car_4",
            5: "car_5",
            6: "car_6",
            7: "invalid id"
        }
        byte_array_copy = int_array.copy()
        byte_helper.set_number(byte_array_copy[8])
        # Check if we have first 5 bytes set by setting last 3 bits to zero and checking the total value is 248
        byte_helper.set_bit(0, 0)
        byte_helper.set_bit(1, 0)
        byte_helper.set_bit(2, 0)
        prepended_1s = byte_helper.number

        object_to_return["car_id_track"] = {
            "constant_bits_should_be_248": prepended_1s, # CAR_ID_TRACK_STARTING = 248 # 11111000
            "car_id": car_id_lookup[int_array[8] ^ 248] # Get last 3 bits of BYTE
        }

        nr_of_bytes_making_up_game_ticks = 4
        game_time_ticks = 0
        for i in range(0, nr_of_bytes_making_up_game_ticks):
            game_time_ticks += int_array[9 + i] << 8 * i

        object_to_return["game_timer_in_micro_seconds"] = game_time_ticks
        object_to_return["race_track_buttons_should_be_0"] = int_array[13]
        object_to_return["checksum"] = int_array[14]
        return object_to_return

    def generate_slot_cars_int_array_for_testing(car_id=0, game_time_in_ms=0, encode_to_byte_array=True):
        int_array = []

        HANDSET_AND_TRACK_STATUS = 255  # IF TRACK ON AND ALL HANDSETS ON

        int_array.append(HANDSET_AND_TRACK_STATUS)
        int_array.extend([255, 255, 255, 255, 255, 255])

        AUX_PORT_CURRENT = 24

        int_array.append(AUX_PORT_CURRENT)

        CAR_ID_TRACK_STARTING = 248  # 11111000
        car_update_value = CAR_ID_TRACK_STARTING ^ car_id
        int_array.append(car_update_value)
        game_time_ticks = int(game_time_in_ms / GAMETICK_IN_MILLISECOND)
        three_byte_array = game_time_ticks.to_bytes(4, 'little')
        for byte in three_byte_array:
            int_array.append(byte)

        # Add 15th bit: http://ssdc.jackaments.com/interface.shtml
        int_array.append(0)  # No buttons pressed

        checksum = ByteHelper.crc8(int_array)
        int_array.append(checksum)

        if encode_to_byte_array:
            return bytes(str(int_array).encode('utf-8'))

        return int_array