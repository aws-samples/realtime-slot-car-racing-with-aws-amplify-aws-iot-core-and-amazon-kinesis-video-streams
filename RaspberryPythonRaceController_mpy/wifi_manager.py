"""
WiFi connection manager for Raspberry Pi Pico 2 W
"""
import network
import time
import config
from logger import log

class WiFiManager:
    """Manages WiFi connection for Pico 2 W"""
    
    def __init__(self):
        """Initialize WiFi manager"""
        self.wlan = network.WLAN(network.STA_IF)
        self.connected = False
        log.info("WiFi manager initialized")
    
    async def connect(self, ssid=None, password=None):
        """Connect to WiFi network"""
        ssid = ssid or config.WIFI_SSID
        password = password or config.WIFI_PASSWORD
        
        if not ssid or not password:
            log.error("WiFi credentials not configured")
            return False
        
        self.wlan.active(True)
        
        if self.wlan.isconnected():
            log.info("Already connected to WiFi")
            self.connected = True
            return True
        
        log.info(f"Connecting to WiFi: {ssid}")
        self.wlan.connect(ssid, password)
        
        # Wait for connection with timeout
        max_wait = 20
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            log.debug(f"Waiting for connection... {max_wait}")
            time.sleep(1)
        
        if self.wlan.status() != 3:
            log.error(f"WiFi connection failed. Status: {self.wlan.status()}")
            self.connected = False
            return False
        
        status = self.wlan.ifconfig()
        log.info(f"Connected to WiFi. IP: {status[0]}")
        self.connected = True
        return True
    
    def is_connected(self):
        """Check if WiFi is connected"""
        return self.wlan.isconnected() and self.connected
    
    def get_status(self):
        """Get WiFi connection status"""
        return {
            "connected": self.is_connected(),
            "status": self.wlan.status(),
            "config": self.wlan.ifconfig() if self.is_connected() else None
        }
    
    def disconnect(self):
        """Disconnect from WiFi"""
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.wlan.active(False)
        self.connected = False
        log.info("Disconnected from WiFi")