"""
Test security validation functions
"""
import sys
sys.path.append('..')

from security import SecurityValidator, RateLimiter

def test_race_id_validation():
    """Test race ID validation"""
    print("Testing race ID validation...")
    
    # Valid UUID
    valid_id = "1bb42be6-24cb-41ac-b1d8-955e7bc2f510"
    assert SecurityValidator.validate_race_id(valid_id), "Valid UUID should pass"
    
    # Invalid formats
    assert not SecurityValidator.validate_race_id("invalid"), "Invalid format should fail"
    assert not SecurityValidator.validate_race_id(""), "Empty string should fail"
    assert not SecurityValidator.validate_race_id(None), "None should fail"
    assert not SecurityValidator.validate_race_id(123), "Number should fail"
    
    print("✓ Race ID validation test passed")

def test_player_id_validation():
    """Test player ID validation"""
    print("Testing player ID validation...")
    
    # Valid player IDs
    assert SecurityValidator.validate_player_id("player123"), "Valid player ID should pass"
    assert SecurityValidator.validate_player_id("user_name"), "Underscore should be allowed"
    assert SecurityValidator.validate_player_id("user-name"), "Dash should be allowed"
    assert SecurityValidator.validate_player_id(""), "Empty string should pass"
    
    # Invalid player IDs
    assert not SecurityValidator.validate_player_id("player@123"), "Special chars should fail"
    assert not SecurityValidator.validate_player_id("a" * 51), "Too long should fail"
    assert not SecurityValidator.validate_player_id(None), "None should fail"
    
    print("✓ Player ID validation test passed")

def test_car_id_validation():
    """Test car ID validation"""
    print("Testing car ID validation...")
    
    # Valid car IDs
    for i in range(1, 7):
        assert SecurityValidator.validate_car_id(str(i)), f"Car ID {i} should be valid"
        assert SecurityValidator.validate_car_id(i), f"Car ID {i} as int should be valid"
    
    # Invalid car IDs
    assert not SecurityValidator.validate_car_id("0"), "Car ID 0 should be invalid"
    assert not SecurityValidator.validate_car_id("7"), "Car ID 7 should be invalid"
    assert not SecurityValidator.validate_car_id("abc"), "Non-numeric should be invalid"
    assert not SecurityValidator.validate_car_id(None), "None should be invalid"
    
    print("✓ Car ID validation test passed")

def test_throttle_validation():
    """Test throttle validation"""
    print("Testing throttle validation...")
    
    # Valid throttle values
    for i in range(0, 101):
        assert SecurityValidator.validate_throttle(i), f"Throttle {i} should be valid"
        assert SecurityValidator.validate_throttle(str(i)), f"Throttle '{i}' should be valid"
    
    # Invalid throttle values
    assert not SecurityValidator.validate_throttle(-1), "Negative throttle should be invalid"
    assert not SecurityValidator.validate_throttle(101), "Throttle > 100 should be invalid"
    assert not SecurityValidator.validate_throttle("abc"), "Non-numeric should be invalid"
    assert not SecurityValidator.validate_throttle(None), "None should be invalid"
    
    print("✓ Throttle validation test passed")

def test_json_validation():
    """Test JSON input validation"""
    print("Testing JSON validation...")
    
    # Valid JSON
    valid_json = '{"key": "value"}'
    data = SecurityValidator.validate_json_input(valid_json)
    assert data == {"key": "value"}, "Valid JSON should parse correctly"
    
    # Invalid JSON
    try:
        SecurityValidator.validate_json_input('{"invalid": json}')
        assert False, "Invalid JSON should raise exception"
    except ValueError:
        pass
    
    # Too large JSON
    large_json = '{"data": "' + 'x' * 2000 + '"}'
    try:
        SecurityValidator.validate_json_input(large_json)
        assert False, "Large JSON should raise exception"
    except ValueError:
        pass
    
    print("✓ JSON validation test passed")

def test_car_update_sanitization():
    """Test car update data sanitization"""
    print("Testing car update sanitization...")
    
    # Valid data
    valid_data = {
        "throttle": "50",
        "lane_change_req": True,
        "brakes_on_req": False,
        "player_id": "player123"
    }
    
    sanitized = SecurityValidator.sanitize_car_update(valid_data)
    assert sanitized["throttle"] == 50, "Throttle should be converted to int"
    assert sanitized["lane_change_req"] == True, "Boolean should be preserved"
    assert sanitized["player_id"] == "player123", "Valid player ID should be preserved"
    
    # Invalid data should be filtered out
    invalid_data = {
        "throttle": "150",  # Too high
        "malicious_attr": "hack",  # Not allowed
        "player_id": "invalid@player"  # Invalid format
    }
    
    sanitized = SecurityValidator.sanitize_car_update(invalid_data)
    assert "throttle" not in sanitized, "Invalid throttle should be filtered"
    assert "malicious_attr" not in sanitized, "Malicious attr should be filtered"
    assert "player_id" not in sanitized, "Invalid player ID should be filtered"
    
    print("✓ Car update sanitization test passed")

def test_rate_limiter():
    """Test rate limiting functionality"""
    print("Testing rate limiter...")
    
    limiter = RateLimiter(max_requests=3, window_ms=1000)
    
    # First 3 requests should be allowed
    for i in range(3):
        assert limiter.is_allowed(1000), f"Request {i+1} should be allowed"
    
    # 4th request should be denied
    assert not limiter.is_allowed(1000), "4th request should be denied"
    
    # After window expires, should be allowed again
    assert limiter.is_allowed(2001), "Request after window should be allowed"
    
    print("✓ Rate limiter test passed")

def run_all_tests():
    """Run all security tests"""
    print("=== Security Tests ===")
    
    try:
        test_race_id_validation()
        test_player_id_validation()
        test_car_id_validation()
        test_throttle_validation()
        test_json_validation()
        test_car_update_sanitization()
        test_rate_limiter()
        
        print("\n✅ All security tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Security test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()