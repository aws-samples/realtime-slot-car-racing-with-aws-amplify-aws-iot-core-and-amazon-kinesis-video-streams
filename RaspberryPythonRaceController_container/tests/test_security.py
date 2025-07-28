"""Tests for security validation."""
import pytest
from src.security import SecurityValidator, RateLimiter


class TestSecurityValidator:
    """Test SecurityValidator class."""
    
    def test_validate_json_input_valid(self):
        """Test valid JSON input."""
        json_str = '{"key": "value"}'
        result = SecurityValidator.validate_json_input(json_str)
        assert result == {"key": "value"}
    
    def test_validate_json_input_invalid(self):
        """Test invalid JSON input."""
        with pytest.raises(ValueError):
            SecurityValidator.validate_json_input('{"invalid": json}')
    
    def test_validate_json_input_too_large(self):
        """Test JSON input too large."""
        large_json = '{"data": "' + 'x' * 2000 + '"}'
        with pytest.raises(ValueError):
            SecurityValidator.validate_json_input(large_json)
    
    def test_validate_race_id_valid(self):
        """Test valid race ID."""
        valid_id = "1bb42be6-24cb-41ac-b1d8-955e7bc2f510"
        assert SecurityValidator.validate_race_id(valid_id)
    
    def test_validate_race_id_invalid(self):
        """Test invalid race ID."""
        assert not SecurityValidator.validate_race_id("invalid")
        assert not SecurityValidator.validate_race_id("")
        assert not SecurityValidator.validate_race_id(None)
        assert not SecurityValidator.validate_race_id(123)
    
    def test_validate_player_id_valid(self):
        """Test valid player ID."""
        assert SecurityValidator.validate_player_id("player123")
        assert SecurityValidator.validate_player_id("user_name")
        assert SecurityValidator.validate_player_id("user-name")
        assert SecurityValidator.validate_player_id("")
    
    def test_validate_player_id_invalid(self):
        """Test invalid player ID."""
        assert not SecurityValidator.validate_player_id("player@123")
        assert not SecurityValidator.validate_player_id("a" * 51)
        assert not SecurityValidator.validate_player_id(None)
    
    def test_validate_car_id_valid(self):
        """Test valid car ID."""
        for i in range(1, 7):
            assert SecurityValidator.validate_car_id(str(i))
            assert SecurityValidator.validate_car_id(i)
    
    def test_validate_car_id_invalid(self):
        """Test invalid car ID."""
        assert not SecurityValidator.validate_car_id("0")
        assert not SecurityValidator.validate_car_id("7")
        assert not SecurityValidator.validate_car_id("abc")
        assert not SecurityValidator.validate_car_id(None)
    
    def test_validate_throttle_valid(self):
        """Test valid throttle values."""
        for i in range(0, 101):
            assert SecurityValidator.validate_throttle(i)
            assert SecurityValidator.validate_throttle(str(i))
    
    def test_validate_throttle_invalid(self):
        """Test invalid throttle values."""
        assert not SecurityValidator.validate_throttle(-1)
        assert not SecurityValidator.validate_throttle(101)
        assert not SecurityValidator.validate_throttle("abc")
        assert not SecurityValidator.validate_throttle(None)
    
    def test_sanitize_car_update_valid(self):
        """Test car update sanitization with valid data."""
        data = {
            "throttle": "50",
            "lane_change_req": True,
            "brakes_on_req": False,
            "player_id": "player123"
        }
        
        sanitized = SecurityValidator.sanitize_car_update(data)
        assert sanitized["throttle"] == 50
        assert sanitized["lane_change_req"] is True
        assert sanitized["player_id"] == "player123"
    
    def test_sanitize_car_update_invalid(self):
        """Test car update sanitization with invalid data."""
        data = {
            "throttle": "150",  # Too high
            "malicious_attr": "hack",  # Not allowed
            "player_id": "invalid@player"  # Invalid format
        }
        
        sanitized = SecurityValidator.sanitize_car_update(data)
        assert "throttle" not in sanitized
        assert "malicious_attr" not in sanitized
        assert "player_id" not in sanitized


class TestRateLimiter:
    """Test RateLimiter class."""
    
    def test_rate_limiter_allows_requests(self):
        """Test rate limiter allows requests within limit."""
        limiter = RateLimiter(max_requests=3, window_ms=1000)
        
        # First 3 requests should be allowed
        for i in range(3):
            assert limiter.is_allowed(1000)
    
    def test_rate_limiter_blocks_excess_requests(self):
        """Test rate limiter blocks excess requests."""
        limiter = RateLimiter(max_requests=3, window_ms=1000)
        
        # First 3 requests allowed
        for i in range(3):
            assert limiter.is_allowed(1000)
        
        # 4th request should be denied
        assert not limiter.is_allowed(1000)
    
    def test_rate_limiter_window_reset(self):
        """Test rate limiter window reset."""
        limiter = RateLimiter(max_requests=3, window_ms=1000)
        
        # Fill up the limit
        for i in range(3):
            assert limiter.is_allowed(1000)
        
        # Should be denied
        assert not limiter.is_allowed(1000)
        
        # After window expires, should be allowed again
        assert limiter.is_allowed(2001)