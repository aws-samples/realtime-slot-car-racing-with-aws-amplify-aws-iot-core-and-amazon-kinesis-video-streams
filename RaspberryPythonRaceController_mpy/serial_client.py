"""
Serial communication client for race track
"""
import asyncio
from machine import UART, Pin
import config
from logger import log

class SerialClient:
    """Handles serial communication with race track"""
    
    def __init__(self):
        """Initialize UART communication"""
        self.uart = UART(0, baudrate=config.UART_BAUDRATE, 
                        tx=Pin(config.UART_TX_PIN), 
                        rx=Pin(config.UART_RX_PIN))
        self.connected = True
        self.send_queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.receive_queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        log.info("Serial client initialized")
    
    async def send_data(self, data):
        """Queue data for sending"""
        try:
            # Validate data format
            if not isinstance(data, list) or len(data) > 255:
                log.warning("Invalid serial data format")
                return
            
            # Validate data values
            if not all(isinstance(x, int) and 0 <= x <= 255 for x in data):
                log.warning("Invalid serial data values")
                return
            
            await self.send_queue.put(data)
            log.debug(f"Queued data for sending")
        except:
            log.error("Send queue full, dropping data")
    
    async def get_received_data(self):
        """Get received data from queue"""
        try:
            return await asyncio.wait_for(self.receive_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    async def _send_worker(self):
        """Worker coroutine for sending data"""
        while True:
            try:
                data = await self.send_queue.get()
                if isinstance(data, list):
                    # Convert int array to bytes
                    byte_data = bytes(data)
                    self.uart.write(byte_data)
                    log.debug(f"Sent {len(byte_data)} bytes")
                await asyncio.sleep_ms(10)  # Small delay between sends
            except Exception as e:
                log.error(f"Send error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _receive_worker(self):
        """Worker coroutine for receiving data"""
        while True:
            try:
                if self.uart.any():
                    data = self.uart.read()
                    if data:
                        # Convert bytes to int array
                        int_array = [x for x in data]
                        await self.receive_queue.put(int_array)
                        log.debug(f"Received {len(int_array)} bytes")
                await asyncio.sleep_ms(10)
            except Exception as e:
                log.error(f"Receive error: {e}")
                await asyncio.sleep_ms(100)
    
    async def start(self):
        """Start send and receive workers"""
        log.info("Starting serial communication workers")
        asyncio.create_task(self._send_worker())
        asyncio.create_task(self._receive_worker())
    
    def is_connected(self):
        """Check if serial connection is active"""
        return self.connected