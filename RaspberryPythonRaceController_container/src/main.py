"""Main application entry point."""
import asyncio
import logging
import signal
import sys
from typing import Optional

from . import config
from .mqtt_client import MQTTClient
from .serial_client import SerialClient
from .race_controller import RaceController

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/var/log/race_controller.log')
    ]
)

logger = logging.getLogger(__name__)


class RaceApplication:
    """Main race application orchestrating all components."""
    
    def __init__(self):
        """Initialize race application."""
        self.mqtt_client = MQTTClient()
        self.serial_client = SerialClient()
        self.race_controller = RaceController()
        self.running = False
        self.tasks = []
        logger.info("Race application initialized")
    
    async def start(self) -> bool:
        """
        Start the race application.
        
        Returns:
            True if started successfully, False otherwise
        """
        logger.info("Starting race application...")
        
        # Connect to MQTT
        if not await self.mqtt_client.connect():
            logger.error("Failed to connect to MQTT")
            return False
        
        # Connect to serial port
        if not await self.serial_client.connect():
            logger.error("Failed to connect to serial port")
            return False
        
        # Subscribe to MQTT topics
        await self._setup_mqtt_subscriptions()
        
        self.running = True
        logger.info("Race application started successfully")
        
        # Start all processing tasks
        self.tasks = [
            asyncio.create_task(self._mqtt_message_processor()),
            asyncio.create_task(self._serial_data_processor()),
            asyncio.create_task(self._track_update_sender()),
            asyncio.create_task(self._lap_time_sender()),
            asyncio.create_task(self._analytics_sender()),
            asyncio.create_task(self._health_monitor())
        ]
        
        return True
    
    async def stop(self):
        """Stop the race application."""
        logger.info("Stopping race application...")
        self.running = False
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.tasks, return_exceptions=True)
        
        # Disconnect clients
        await self.mqtt_client.disconnect()
        await self.serial_client.disconnect()
        
        logger.info("Race application stopped")
    
    async def _setup_mqtt_subscriptions(self):
        """Set up MQTT topic subscriptions."""
        await self.mqtt_client.subscribe(
            config.GAME_STATE_UPDATE_TOPIC,
            self._handle_game_state_update
        )
        await self.mqtt_client.subscribe(
            config.CAR_CONTROL_UPDATE_TOPIC,
            self._handle_car_control_update
        )
    
    async def _handle_game_state_update(self, topic: str, payload: str):
        """
        Handle game state update messages.
        
        Args:
            topic: MQTT topic
            payload: Message payload
        """
        await self.race_controller.handle_race_update(payload)
    
    async def _handle_car_control_update(self, topic: str, payload: str):
        """
        Handle car control update messages.
        
        Args:
            topic: MQTT topic
            payload: Message payload
        """
        await self.race_controller.handle_car_update(payload)
    
    async def _mqtt_message_processor(self):
        """Process MQTT messages."""
        logger.info("Starting MQTT message processor")
        
        try:
            await self.mqtt_client.start_message_loop()
        except Exception as e:
            logger.error(f"MQTT message processor error: {e}")
            self.running = False
    
    async def _serial_data_processor(self):
        """Process data from serial connection to track."""
        logger.info("Starting serial data processor")
        
        while self.running:
            try:
                data = await self.serial_client.get_received_data()
                if data and len(data) >= 15:  # Expected track data length
                    await self.race_controller.handle_track_data(data)
                
                await asyncio.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Serial data processing error: {e}")
                await asyncio.sleep(0.1)
    
    async def _track_update_sender(self):
        """Send control updates to race track."""
        logger.info("Starting track update sender")
        
        while self.running:
            try:
                # Always send current array to maintain communication
                int_array = self.race_controller.get_current_int_array()
                await self.serial_client.send_data(int_array)
                
                await asyncio.sleep(config.SERIAL_REFRESH_RATE_MS / 1000)
                
            except Exception as e:
                logger.error(f"Track update sender error: {e}")
                await asyncio.sleep(0.1)
    
    async def _lap_time_sender(self):
        """Send lap times to MQTT."""
        logger.info("Starting lap time sender")
        
        while self.running:
            try:
                lap_time = await self.race_controller.get_lap_time()
                if lap_time:
                    await self.mqtt_client.publish(
                        config.LAP_TIME_TOPIC,
                        lap_time.to_json()
                    )
                    logger.info(f"Sent lap time: {lap_time}")
                
                await asyncio.sleep(config.MQTT_REFRESH_RATE_MS / 1000)
                
            except Exception as e:
                logger.error(f"Lap time sender error: {e}")
                await asyncio.sleep(0.1)
    
    async def _analytics_sender(self):
        """Send race analytics to MQTT."""
        logger.info("Starting analytics sender")
        
        while self.running:
            try:
                analytics = await self.race_controller.get_analytics()
                if analytics:
                    await self.mqtt_client.publish(
                        config.RACE_ANALYTICS_TOPIC,
                        analytics.to_json()
                    )
                    logger.debug("Sent analytics data")
                
                await asyncio.sleep(config.ANALYTICS_REFRESH_RATE_MS / 1000)
                
            except Exception as e:
                logger.error(f"Analytics sender error: {e}")
                await asyncio.sleep(0.1)
    
    async def _health_monitor(self):
        """Monitor system health and reconnect if needed."""
        logger.info("Starting health monitor")
        
        while self.running:
            try:
                # Check MQTT connection
                if not self.mqtt_client.is_connected():
                    logger.warning("MQTT disconnected, attempting reconnect...")
                    await self.mqtt_client.connect()
                    if self.mqtt_client.is_connected():
                        await self._setup_mqtt_subscriptions()
                
                # Check serial connection
                if not self.serial_client.is_connected():
                    logger.warning("Serial disconnected, attempting reconnect...")
                    await self.serial_client.connect()
                
                # Log status periodically
                logger.info(f"Health check - MQTT: {self.mqtt_client.is_connected()}, "
                           f"Serial: {self.serial_client.is_connected()}")
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(5)


async def main():
    """Main entry point."""
    logger.info("=== Race Controller Starting ===")
    logger.info(f"AWS IoT Endpoint: {config.AWS_IOT_ENDPOINT}")
    logger.info(f"Serial Port: {config.SERIAL_PORT}")
    
    app = RaceApplication()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(app.stop())
    
    # Register signal handlers
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, lambda s, f: signal_handler())
    
    try:
        if await app.start():
            # Keep running until stopped
            while app.running:
                await asyncio.sleep(1)
        else:
            logger.error("Failed to start application")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    except Exception as e:
        logger.error(f"Application error: {e}")
        return 1
    finally:
        await app.stop()
    
    logger.info("=== Race Controller Stopped ===")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))