from typing import List
import serial
import RPi.GPIO as GPIO
import utils.constants as constants

import time

from utils.client import Client

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

''''
THIS CLASS IS DEPRECATED - ONLY USED IN CASE WE WANT TO EXPERIMENT WITH THIS AGAIN
'''

class SerialClient(Client):
    def __init__(self, RE_PIN=13, DE_PIN=11, port="/dev/serial0") -> None:
        super().__init__(client_type=constants.CLIENT_OPTIONS["SERIAL"])
        self.RE_PIN = RE_PIN
        self.DE_PIN = DE_PIN

        GPIO.setup(self.DE_PIN, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.RE_PIN, GPIO.OUT, initial=GPIO.HIGH)

        self.port = port
        self.ser = serial.Serial(
            port="/dev/serial0",
            baudrate=19200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            rtscts=True
        )
        self._connected = True

    def send_payload(self, payload):
        if self._client_type not in constants.CLIENT_OPTIONS.values():
            raise ValueError(f"Invalid Client Type: {self._client_type}")

        self.send_and_recv_int_array(payload)


    def send_and_recv_payload(self, payload) -> int:
        """
        Add timeouts before this function when used. time.sleep(0.001) is usually enough
        """
        data: List[int] = payload.int_array
        recv_handler = payload.recv_handler

        GPIO.output(self.DE_PIN, GPIO.HIGH)
        GPIO.output(self.RE_PIN, GPIO.HIGH)
        time.sleep(0.01)
        self.ser.write(data)
        time.sleep(0.01)
        GPIO.output(self.DE_PIN, GPIO.LOW)
        GPIO.output(self.RE_PIN, GPIO.LOW)
        resp = bytearray(self.ser.read(15))
        if resp:
            parsed_resp = [x for x in resp]
            recv_handler(parsed_resp)

    def __del__(self):
        self.ser.close()
        GPIO.cleanup()
