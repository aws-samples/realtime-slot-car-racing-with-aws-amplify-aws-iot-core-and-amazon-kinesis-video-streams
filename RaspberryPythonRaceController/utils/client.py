from abc import abstractmethod
import utils.constants as constants

class Client:
    def __init__(self, client_type) -> None:
        self._connected = False
        self._client_type = client_type

    @abstractmethod
    def send_payload(self, payload):
        raise NotImplementedError("Tried to send payload, but not implemented for client")