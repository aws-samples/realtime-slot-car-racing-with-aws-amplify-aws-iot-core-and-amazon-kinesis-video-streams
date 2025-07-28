"""
Main application for Raspberry Pi Pico 2 W Race Controller
"""
import asyncio
import config
from compat import ticks_ms, ticks_diff
from logger import log
from wifi_manager import WiFiManager
from mqtt_client import MQTTClientAsync
from serial_client import SerialClient
from race_controller import RaceController
from secure_config import SecureConfig

class RaceApplication:
    """Main race application orchestrating all components"""
    
    def __init__(self):
        """Initialize race application"""
        self.wifi = WiFiManager()
        self.mqtt = MQTTClientAsync()
        self.serial = SerialClient()
        self.race_controller = RaceController()
        self.running = False
        log.info("Race application initialized")
    
    async def start(self):
        """Start the race application"""
        log.info("Starting race application...")
        
        # Validate configuration
        if not SecureConfig.validate_config():
            log.error("Configuration validation failed")
            return False
        
        # Connect to WiFi
        if not await self.wifi.connect():
            log.error("Failed to connect to WiFi")
            return False
        
        # Connect to MQTT
        await self.mqtt.connect()
        if not self.mqtt.is_connected():
            log.error("Failed to connect to MQTT")
            return False
        
        # Start all services
        await self.mqtt.start()
        await self.serial.start()
        
        self.running = True
        log.info("Race application started successfully")
        
        # Start main processing loops
        await asyncio.gather(
            self._mqtt_message_processor(),
            self._serial_data_processor(),
            self._track_update_sender(),
            self._lap_time_sender(),
            self._analytics_sender(),
            self._status_monitor()
        )
    
    async def _mqtt_message_processor(self):
        """Process incoming MQTT messages"""
        log.info("Starting MQTT message processor")
        
        while self.running:
            try:
                message = await self.mqtt.get_message()
                if message:
                    topic, payload = message
                    
                    if topic == config.GAME_STATE_UPDATE_TOPIC:
                        await self.race_controller.handle_race_update(payload)
                    elif topic == config.CAR_CONTROL_UPDATE_TOPIC:
                        await self.race_controller.handle_car_update(payload)
                    elif topic == config.TRACK_MQTT_TOPIC_SUB:
                        # Handle track data if using MQTT for track communication
                        pass
                
                await asyncio.sleep_ms(10)
                
            except Exception as e:
                log.error(f"MQTT message processing error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _serial_data_processor(self):
        """Process data from serial connection to track"""
        log.info("Starting serial data processor")
        
        while self.running:
            try:
                data = await self.serial.get_received_data()
                if data and len(data) >= 15:  # Expected track data length
                    await self.race_controller.handle_track_data(data)
                
                await asyncio.sleep_ms(10)
                
            except Exception as e:
                log.error(f"Serial data processing error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _track_update_sender(self):
        """Send control updates to race track"""
        log.info("Starting track update sender")
        last_send = ticks_ms()
        
        while self.running:
            try:
                current_time = ticks_ms()
                
                if ticks_diff(current_time, last_send) >= config.SERIAL_REFRESH_RATE_MS:
                    # Always send current array to maintain communication
                    int_array = self.race_controller.get_current_int_array()
                    await self.serial.send_data(int_array)
                    last_send = current_time
                
                await asyncio.sleep_ms(10)
                
            except Exception as e:
                log.error(f"Track update sender error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _lap_time_sender(self):
        """Send lap times to MQTT"""
        log.info("Starting lap time sender")
        last_send = ticks_ms()
        
        while self.running:
            try:
                current_time = ticks_ms()
                
                if ticks_diff(current_time, last_send) >= config.MQTT_REFRESH_RATE_MS:
                    lap_time = await self.race_controller.get_lap_time()
                    if lap_time:
                        await self.mqtt.publish(config.LAP_TIME_TOPIC, lap_time.to_json())
                        log.info(f"Sent lap time: {lap_time}")
                    last_send = current_time
                
                await asyncio.sleep_ms(50)
                
            except Exception as e:
                log.error(f"Lap time sender error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _analytics_sender(self):
        """Send race analytics to MQTT"""
        log.info("Starting analytics sender")
        last_send = ticks_ms()
        
        while self.running:
            try:
                current_time = ticks_ms()
                
                if ticks_diff(current_time, last_send) >= config.ANALYTICS_REFRESH_RATE_MS:
                    analytics = await self.race_controller.get_analytics()
                    if analytics:
                        await self.mqtt.publish(config.RACE_ANALYTICS_TOPIC, analytics.to_json())
                        log.debug(f"Sent analytics data")
                    last_send = current_time
                
                await asyncio.sleep_ms(100)
                
            except Exception as e:
                log.error(f"Analytics sender error: {e}")
                await asyncio.sleep_ms(100)
    
    async def _status_monitor(self):
        """Monitor system status and reconnect if needed"""
        log.info("Starting status monitor")
        
        while self.running:
            try:
                # Check WiFi connection
                if not self.wifi.is_connected():
                    log.warning("WiFi disconnected, attempting reconnect...")
                    await self.wifi.connect()
                
                # Check MQTT connection
                if not self.mqtt.is_connected():
                    log.warning("MQTT disconnected, attempting reconnect...")
                    await self.mqtt.connect()
                
                # Log status periodically
                if ticks_ms() % 30000 < 1000:  # Every 30 seconds
                    wifi_status = self.wifi.get_status()
                    log.info(f"Status - WiFi: {wifi_status['connected']}, "
                            f"MQTT: {self.mqtt.is_connected()}, "
                            f"Serial: {self.serial.is_connected()}")
                
                await asyncio.sleep_ms(5000)  # Check every 5 seconds
                
            except Exception as e:
                log.error(f"Status monitor error: {e}")
                await asyncio.sleep_ms(5000)
    
    async def stop(self):
        """Stop the race application"""
        log.info("Stopping race application...")
        self.running = False
        
        await self.mqtt.disconnect()
        self.wifi.disconnect()
        
        log.info("Race application stopped")

async def main():
    """Main entry point"""
    log.info("=== Raspberry Pi Pico 2 W Race Controller ===")
    log.info(f"Firmware: MicroPython")
    log.info(f"Target: {config.AWS_IOT_ENDPOINT}")
    
    app = RaceApplication()
    
    try:
        await app.start()
    except KeyboardInterrupt:
        log.info("Received interrupt signal")
    except Exception as e:
        log.error(f"Application error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())