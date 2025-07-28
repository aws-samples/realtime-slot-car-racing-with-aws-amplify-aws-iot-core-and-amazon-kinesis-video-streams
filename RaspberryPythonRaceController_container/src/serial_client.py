"""Serial communication client for race track."""
import asyncio
import logging
import serial
from typing import Optional, List
from serial.serialutil import SerialException

from . import config

logger = logging.getLogger(__name__)


class SerialClient:
    """Handles serial communication with race track."""
    
    def __init__(self):
        """Initialize serial client."""
        self.serial_port: Optional[serial.Serial] = None
        self.connected = False
        self.send_queue: asyncio.Queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.receive_queue: asyncio.Queue = asyncio.Queue(maxsize=config.MAX_QUEUE_SIZE)
        logger.info("Serial client initialized")
    
    async def connect(self) -> bool:
        """
        Connect to serial port.
        
        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.serial_port = serial.Serial(
                port=config.SERIAL_PORT,
                baudrate=config.SERIAL_BAUDRATE,
                timeout=1
            )
            self.connected = True
            logger.info(f"Connected to serial port: {config.SERIAL_PORT}")
            return True
            
        except SerialException as e:
            logger.error(f"Serial connection failed: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from serial port."""
        if self.serial_port and self.connected:
            try:
                self.serial_port.close()
                self.connected = False
                logger.info("Disconnected from serial port")
            except Exception as e:
                logger.error(f"Error disconnecting serial: {e}")
    
    async def send_data(self, data: List[int]):
        """
        Queue data for sending.
        
        Args:
            data: List of integers to send
        """
        try:
            # Validate data format
            if not isinstance(data, list) or len(data) > 255:
                logger.warning("Invalid serial data format")
                return
            
            # Validate data values
            if not all(isinstance(x, int) and 0 <= x <= 255 for x in data):
                logger.warning("Invalid serial data values")
                return
            
            await self.send_queue.put(data)
            logger.debug("Queued data for sending")
        except asyncio.QueueFull:
            logger.error("Send queue full, dropping data")
    
    async def get_received_data(self) -> Optional[List[int]]:
        """
        Get received data from queue.
        
        Returns:
            List of received integers or None if no data
        """
        try:
            return await asyncio.wait_for(self.receive_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    async def start_send_worker(self):
        """Start the send worker coroutine."""
        logger.info("Starting serial send worker")
        
        while self.connected:
            try:
                data = await self.send_queue.get()
                if self.serial_port and self.connected:
                    # Convert int array to bytes
                    byte_data = bytes(data)
                    await asyncio.get_event_loop().run_in_executor(
                        None, self.serial_port.write, byte_data
                    )
                    logger.debug(f"Sent {len(byte_data)} bytes")
                await asyncio.sleep(0.01)  # Small delay between sends
            except Exception as e:
                logger.error(f"Send error: {e}")
                await asyncio.sleep(0.1)
    
    async def start_receive_worker(self):
        """Start the receive worker coroutine."""
        logger.info("Starting serial receive worker")
        
        while self.connected:
            try:
                if self.serial_port and self.connected:
                    # Check if data is available
                    if self.serial_port.in_waiting > 0:
                        data = await asyncio.get_event_loop().run_in_executor(
                            None, self.serial_port.read, self.serial_port.in_waiting
                        )
                        if data:
                            # Convert bytes to int array
                            int_array = list(data)
                            await self.receive_queue.put(int_array)
                            logger.debug(f"Received {len(int_array)} bytes")
                await asyncio.sleep(0.01)
            except Exception as e:
                logger.error(f"Receive error: {e}")
                await asyncio.sleep(0.1)
    
    async def start(self):
        """Start send and receive workers."""
        if not self.connected:
            raise RuntimeError("Serial client not connected")
        
        logger.info("Starting serial communication workers")
        await asyncio.gather(
            self.start_send_worker(),
            self.start_receive_worker()
        )
    
    def is_connected(self) -> bool:
        """
        Check if serial connection is active.
        
        Returns:
            True if connected, False otherwise
        """
        return self.connected and self.serial_port is not None