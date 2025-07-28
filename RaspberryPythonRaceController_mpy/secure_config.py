"""
Secure configuration loader
"""
import config
from logger import log

class SecureConfig:
    """Load configuration from secure sources"""
    
    @staticmethod
    def load_wifi_credentials():
        """Load WiFi credentials from secure source"""
        # In production, load from:
        # - Environment variables
        # - Encrypted config file
        # - Hardware security module
        
        ssid = config.WIFI_SSID
        password = config.WIFI_PASSWORD
        
        if not ssid or not password:
            log.error("WiFi credentials not configured")
            return None, None
        
        return ssid, password
    
    @staticmethod
    def load_aws_config():
        """Load AWS IoT configuration from secure source"""
        endpoint = config.AWS_IOT_ENDPOINT
        
        if not endpoint:
            log.error("AWS IoT endpoint not configured")
            return None
        
        return endpoint
    
    @staticmethod
    def validate_config():
        """Validate all required configuration"""
        errors = []
        
        if not config.WIFI_SSID:
            errors.append("WIFI_SSID not set")
        if not config.WIFI_PASSWORD:
            errors.append("WIFI_PASSWORD not set")
        if not config.AWS_IOT_ENDPOINT:
            errors.append("AWS_IOT_ENDPOINT not set")
        
        if errors:
            log.error(f"Configuration errors: {', '.join(errors)}")
            return False
        
        return True