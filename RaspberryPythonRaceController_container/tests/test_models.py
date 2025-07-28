"""Tests for data models."""
import pytest
import json
from src.models import Car, LapTime, RaceAnalytics


class TestCar:
    """Test Car model."""
    
    def test_car_creation(self):
        """Test car creation with valid data."""
        car = Car(number=1)
        assert car.number == 1
        assert car.player_id == ""
        assert car.throttle == 0
        assert not car.lane_change_req
        assert not car.brakes_on_req
        assert car.latest_finish_time == 0
    
    def test_car_invalid_number(self):
        """Test car creation with invalid number."""
        with pytest.raises(ValueError):
            Car(number=0)
        
        with pytest.raises(ValueError):
            Car(number=7)
    
    def test_car_invalid_throttle(self):
        """Test car creation with invalid throttle."""
        with pytest.raises(ValueError):
            Car(number=1, throttle=-1)
        
        with pytest.raises(ValueError):
            Car(number=1, throttle=101)


class TestLapTime:
    """Test LapTime model."""
    
    def test_laptime_creation(self):
        """Test lap time creation."""
        lap_time = LapTime("race-123", "player-456", 30000)
        assert lap_time.race_id == "race-123"
        assert lap_time.player_id == "player-456"
        assert lap_time.time_ms == 30000
        assert lap_time.timestamp is not None
    
    def test_laptime_to_json(self):
        """Test lap time JSON serialization."""
        lap_time = LapTime("race-123", "player-456", 30000, timestamp=1234567890.0)
        json_str = lap_time.to_json()
        data = json.loads(json_str)
        
        assert data['raceId'] == "race-123"
        assert data['playerId'] == "player-456"
        assert data['timeInMilliSec'] == 30000
        assert data['timestamp'] == 1234567890.0
    
    def test_laptime_str(self):
        """Test lap time string representation."""
        lap_time = LapTime("race-123", "player-456", 30000)
        assert str(lap_time) == "race-123:player-456:30000"


class TestRaceAnalytics:
    """Test RaceAnalytics model."""
    
    def test_analytics_creation(self):
        """Test analytics creation."""
        analytics = RaceAnalytics("race-123", True, 50, 3)
        assert analytics.race_id == "race-123"
        assert analytics.track_power_status is True
        assert analytics.port_current == 50
        assert analytics.active_cars == 3
        assert analytics.timestamp is not None
    
    def test_analytics_to_json(self):
        """Test analytics JSON serialization."""
        analytics = RaceAnalytics("race-123", True, 50, 3, timestamp=1234567890.0)
        json_str = analytics.to_json()
        data = json.loads(json_str)
        
        assert data['raceId'] == "race-123"
        assert data['trackPowerStatus'] is True
        assert data['portCurrent'] == 50
        assert data['activeCars'] == 3
        assert data['timestamp'] == 1234567890.0