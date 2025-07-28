"""
Security utilities and validation functions
"""
import json
import re
from logger import log

class SecurityValidator:
    """Input validation and sanitization"""
    
    # Allowed attributes for car updates
    ALLOWED_CAR_ATTRIBUTES = {
        'throttle', 'lane_change_req', 'brakes_on_req', 'player_id'
    }
    
    # Maximum string lengths
    MAX_PLAYER_ID_LENGTH = 50
    MAX_RACE_ID_LENGTH = 100
    MAX_JSON_SIZE = 1024
    
    @staticmethod
    def validate_json_input(json_string):
        """Validate and parse JSON input safely"""
        if not isinstance(json_string, str):
            raise ValueError("Input must be string")
        
        if len(json_string) > SecurityValidator.MAX_JSON_SIZE:
            raise ValueError("JSON input too large")
        
        try:
            data = json.loads(json_string)
            if not isinstance(data, dict):
                raise ValueError("JSON must be object")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    
    @staticmethod
    def validate_race_id(race_id):
        """Validate race ID format"""
        if not isinstance(race_id, str):
            return False
        if len(race_id) > SecurityValidator.MAX_RACE_ID_LENGTH:
            return False
        # UUID format validation
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, race_id))
    
    @staticmethod
    def validate_player_id(player_id):
        """Validate player ID"""
        if not isinstance(player_id, str):
            return False
        if len(player_id) > SecurityValidator.MAX_PLAYER_ID_LENGTH:
            return False
        # Alphanumeric and basic chars only
        return bool(re.match(r'^[a-zA-Z0-9_-]*$', player_id))
    
    @staticmethod
    def validate_car_id(car_id):
        """Validate car ID range"""
        try:
            car_num = int(car_id)
            return 1 <= car_num <= 6
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_throttle(throttle):
        """Validate throttle value"""
        try:
            throttle_val = int(throttle)
            return 0 <= throttle_val <= 100
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_car_update(data):
        """Sanitize car update data"""
        sanitized = {}
        
        for key, value in data.items():
            if key not in SecurityValidator.ALLOWED_CAR_ATTRIBUTES:
                continue
                
            if key == 'throttle':
                if SecurityValidator.validate_throttle(value):
                    sanitized[key] = int(value)
            elif key in ['lane_change_req', 'brakes_on_req']:
                sanitized[key] = bool(value)
            elif key == 'player_id':
                if SecurityValidator.validate_player_id(value):
                    sanitized[key] = str(value)
        
        return sanitized

class RateLimiter:
    """Simple rate limiting"""
    
    def __init__(self, max_requests=10, window_ms=1000):
        self.max_requests = max_requests
        self.window_ms = window_ms
        self.requests = []
    
    def is_allowed(self, current_time_ms):
        """Check if request is within rate limit"""
        # Remove old requests outside window
        cutoff = current_time_ms - self.window_ms
        self.requests = [req for req in self.requests if req > cutoff]
        
        if len(self.requests) >= self.max_requests:
            return False
        
        self.requests.append(current_time_ms)
        return True