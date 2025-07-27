"""
Test script for data models
"""
import sys
sys.path.append('..')

import json
from models import Car, LapTime, RaceAnalytics

def test_car_model():
    """Test Car model functionality"""
    print("Testing Car model...")
    
    # Test initialization
    car = Car(number=1, player_id="player123", throttle=50)
    assert car.number == 1, "Car number should be set"
    assert car.player_id == "player123", "Player ID should be set"
    assert car.throttle == 50, "Throttle should be set"
    
    # Test equality
    car2 = Car(number=1, player_id="player123", throttle=50)
    assert car == car2, "Cars with same attributes should be equal"
    
    car3 = Car(number=2, player_id="player123", throttle=50)
    assert car != car3, "Cars with different numbers should not be equal"
    
    print("✓ Car model test passed")

def test_lap_time_model():
    """Test LapTime model functionality"""
    print("Testing LapTime model...")
    
    # Test initialization
    lap_time = LapTime("race123", "player456", 45000)
    assert lap_time.race_id == "race123", "Race ID should be set"
    assert lap_time.player_id == "player456", "Player ID should be set"
    assert lap_time.lap_time_ms == 45000, "Lap time should be set"
    
    # Test JSON conversion
    json_str = lap_time.to_json()
    data = json.loads(json_str)
    
    assert data["raceId"] == "race123", "JSON should contain race ID"
    assert data["playerId"] == "player456", "JSON should contain player ID"
    assert data["timeInMilliSec"] == 45000, "JSON should contain lap time"
    
    # Test equality
    lap_time2 = LapTime("race123", "player456", 45000)
    assert lap_time == lap_time2, "Lap times with same data should be equal"
    
    lap_time3 = LapTime("race123", "player456", 46000)
    assert lap_time != lap_time3, "Lap times with different times should not be equal"
    
    print("✓ LapTime model test passed")

def test_race_analytics_model():
    """Test RaceAnalytics model functionality"""
    print("Testing RaceAnalytics model...")
    
    # Test initialization
    drive_array = [255, 200, 150, 100, 50, 0]
    slotcar_array = [1, 2, 3, 4, 5, 6]
    
    analytics = RaceAnalytics("race789", drive_array, slotcar_array)
    assert analytics.race_id == "race789", "Race ID should be set"
    assert analytics.drive_int_array == drive_array, "Drive array should be set"
    assert analytics.slotcar_int_array == slotcar_array, "Slotcar array should be set"
    
    # Test JSON conversion
    json_str = analytics.to_json()
    data = json.loads(json_str)
    
    assert data["raceId"] == "race789", "JSON should contain race ID"
    assert data["driveIntArray"] == str(drive_array), "JSON should contain drive array"
    assert data["slotcarIntArray"] == str(slotcar_array), "JSON should contain slotcar array"
    assert "timestamp" in data, "JSON should contain timestamp"
    
    print("✓ RaceAnalytics model test passed")

def run_all_tests():
    """Run all model tests"""
    print("=== Model Tests ===")
    
    try:
        test_car_model()
        test_lap_time_model()
        test_race_analytics_model()
        
        print("\n✅ All model tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    run_all_tests()