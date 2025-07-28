"""Security validation utilities."""
import json
import re
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class SecurityValidator:
    """Input validation and sanitization utilities."""
    
    # Allowed attributes for car updates
    ALLOWED_CAR_ATTRIBUTES = {'throttle', 'lane_change_req', 'brakes_on_req', 'player_id'}
    
    # Maximum string lengths
    MAX_PLAYER_ID_LENGTH = 50
    MAX_RACE_ID_LENGTH = 100
    MAX_JSON_SIZE = 1024
    
    @staticmethod
    def validate_json_input(json_string: str) -> Dict[str, Any]:
        """
        Validate and parse JSON input safely.
        
        Args:
            json_string: JSON string to validate
            
        Returns:
            Parsed JSON data
            
        Raises:
            ValueError: If JSON is invalid or too large
        """
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
    def validate_race_id(race_id: Optional[str]) -> bool:
        """
        Validate race ID format (UUID).
        
        Args:
            race_id: Race ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(race_id, str):
            return False
        if len(race_id) > SecurityValidator.MAX_RACE_ID_LENGTH:
            return False
        # UUID format validation
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, race_id, re.IGNORECASE))
    
    @staticmethod
    def validate_player_id(player_id: Optional[str]) -> bool:
        """
        Validate player ID format.
        
        Args:
            player_id: Player ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(player_id, str):
            return False
        if len(player_id) > SecurityValidator.MAX_PLAYER_ID_LENGTH:
            return False
        # Alphanumeric and basic chars only
        return bool(re.match(r'^[a-zA-Z0-9_-]*$', player_id))
    
    @staticmethod
    def validate_car_id(car_id: Any) -> bool:
        """
        Validate car ID range (1-6).
        
        Args:
            car_id: Car ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            car_num = int(car_id)
            return 1 <= car_num <= 6
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_throttle(throttle: Any) -> bool:
        """
        Validate throttle value (0-100).
        
        Args:
            throttle: Throttle value to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            throttle_val = int(throttle)
            return 0 <= throttle_val <= 100
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_car_update(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize car update data.
        
        Args:
            data: Raw car update data
            
        Returns:
            Sanitized car update data
        """
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
    """Simple rate limiting utility."""
    
    def __init__(self, max_requests: int = 10, window_ms: int = 1000):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in window
            window_ms: Time window in milliseconds
        """
        self.max_requests = max_requests
        self.window_ms = window_ms
        self.requests = []
    
    def is_allowed(self, current_time_ms: int) -> bool:
        """
        Check if request is within rate limit.
        
        Args:
            current_time_ms: Current time in milliseconds
            
        Returns:
            True if allowed, False if rate limited
        """
        # Remove old requests outside window
        cutoff = current_time_ms - self.window_ms
        self.requests = [req for req in self.requests if req > cutoff]
        
        if len(self.requests) >= self.max_requests:
            return False
        
        self.requests.append(current_time_ms)
        return True