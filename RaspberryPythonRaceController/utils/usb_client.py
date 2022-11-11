from typing import List
import serial

from utils.client import Client
import utils.constants as constants

# usually /dev/ttyACM1

class USBClient(Client):
    def __init__(
        self,
        port="/dev/ttyUSB0",
        baudrate=19200,
        timeout=1,
    ):
        super().__init__(client_type=constants.CLIENT_OPTIONS["USB"])
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.race_stopped = False
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout,
            )
            self._connected = True
        except Exception as e:
            print(f"Error connecting to USB serial - {e}")

    def send_payload(self, payload, racer_helper=None):
        if self._client_type not in constants.CLIENT_OPTIONS.values():
            raise ValueError(f"Invalid Client Type: {self._client_type}")

        self.send_and_recv_int_array(payload, racer_helper)


    def send_and_recv_int_array(self, payload, racer_helper=None) -> int:
        """
        Add timeouts before this function when used. time.sleep(0.001) is usually enough
        """
        data: List[int] = payload.get('int_array')
        recv_handler = payload.get('recv_handler')
        if len(data) != 9:
            raise Exception("Outgoing array must be length 9")


        drive_packet_indicates_ongoing = self.drive_packet_indicates_race_ongoing(data)

        # Don't do anything if race is stopped, and no signal to start race
        if self.race_stopped and not drive_packet_indicates_ongoing:
            return

        # Otherwise - write
        resp = self.ser.write(bytes(data))

        if resp and resp > 0:
            resp = bytearray(self.ser.read(15))
            parsed_resp = [x for x in resp]
            recv_handler(parsed_resp)

            print(f"{data} => {parsed_resp}")

            if racer_helper is not None:
                race_tuple = (data, parsed_resp)
                racer_helper.raceAnalyticsItems.append(race_tuple)

            # Set the race to stopped after sending the array
            self.race_stopped = drive_packet_indicates_ongoing == False

    def drive_packet_indicates_race_ongoing(self, int_array):
        '''
        Use 8th byte (index 7) from driver packet to determine if we should
        stop the race. We need to do this, because we need to send a final packet to the
        track to indicidate it should be stopped.
        '''
        byte_8 = int_array[7]
        bit_7_set = byte_8 >> 7 & 1 != 0
        bit_6_set = byte_8 >> 6 & 1 != 0
        # Green: 1, Red: 0 => Race is ongoing!
        return bit_7_set == True and bit_6_set == False

    def __del__(self):
        self.ser.close()