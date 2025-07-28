"""Tests for race controller."""
import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from src.race_controller import RaceController, ByteHelper
from src import config


class TestByteHelper:
    """Test ByteHelper class."""
    
    def test_set_bit(self):
        """Test bit setting."""
        helper = ByteHelper()
        helper.set_bit(0, 1)
        assert helper.number == 1
        
        helper.set_bit(1, 1)
        assert helper.number == 3
        
        helper.set_bit(0, 0)
        assert helper.number == 2
    
    def test_set_car_speed(self):
        """Test car speed setting."""
        helper = ByteHelper()
        helper.set_car_speed(15)
        assert helper.number == 15
        
        helper.set_bit(7, 1)  # Set high bit
        helper.set_car_speed(10)
        assert helper.number == (128 | 10)  # High bit preserved
    
    def test_ones_complement(self):
        """Test one's complement."""
        helper = ByteHelper()
        helper.number = 170  # 10101010
        assert helper.get_int_ones_complement() == 85  # 01010101
    
    def test_crc8(self):
        """Test CRC8 calculation."""
        data = [255, 255, 255, 255, 255, 255, 255, 0]
        crc = ByteHelper.crc8(data)
        assert isinstance(crc, int)
        assert 0 <= crc <= 255


class TestRaceController:
    """Test RaceController class."""
    
    @pytest.fixture
    def controller(self):
        """Create race controller instance."""
        return RaceController()
    
    def test_initialization(self, controller):
        """Test controller initialization."""
        assert controller.current_race_id == config.INITIAL_RACE_ID
        assert len(controller.cars) == config.TOTAL_NUMBER_OF_CARS
        assert controller.current_race_state is None
        assert not controller.track_power_status
    
    @pytest.mark.asyncio
    async def test_handle_race_update_valid(self, controller):
        """Test handling valid race update."""
        race_data = {
            "gameState": "lobby",
            "raceId": "2bb42be6-24cb-41ac-b1d8-955e7bc2f511",
            "carClaims": []
        }
        
        await controller.handle_race_update(json.dumps(race_data))
        
        assert controller.current_race_id == "2bb42be6-24cb-41ac-b1d8-955e7bc2f511"
        assert controller.current_race_state == "lobby"
    
    @pytest.mark.asyncio
    async def test_handle_race_update_invalid_state(self, controller):
        """Test handling race update with invalid state."""
        race_data = {
            "gameState": "invalid_state",
            "raceId": "2bb42be6-24cb-41ac-b1d8-955e7bc2f511"
        }
        
        await controller.handle_race_update(json.dumps(race_data))
        
        # State should not change
        assert controller.current_race_state is None
    
    @pytest.mark.asyncio
    async def test_handle_car_update_valid(self, controller):
        """Test handling valid car update."""
        # Set up race first
        controller.current_race_id = "3bb42be6-24cb-41ac-b1d8-955e7bc2f512"
        
        car_data = {
            "raceId": "3bb42be6-24cb-41ac-b1d8-955e7bc2f512",
            "carId": "1",
            "player_id": "player123",
            "throttle": 75,
            "lane_change_req": True,
            "brakes_on_req": False
        }
        
        await controller.handle_car_update(json.dumps(car_data))
        
        car = controller.cars[0]
        assert car.player_id == "player123"
        assert car.throttle == 75
        assert car.lane_change_req is True
        assert car.brakes_on_req is False
    
    @pytest.mark.asyncio
    async def test_handle_car_update_invalid_race_id(self, controller):
        """Test handling car update with invalid race ID."""
        controller.current_race_id = "valid-race-id"
        
        car_data = {
            "raceId": "invalid-race-id",
            "carId": "1",
            "throttle": 50
        }
        
        # Should not update car
        original_throttle = controller.cars[0].throttle
        await controller.handle_car_update(json.dumps(car_data))
        assert controller.cars[0].throttle == original_throttle
    
    @pytest.mark.asyncio
    async def test_handle_track_data_valid(self, controller):
        """Test handling valid track data."""
        controller.current_race_state = config.RACE_STATE_GREEN_FLAG
        controller.current_race_id = "4bb42be6-24cb-41ac-b1d8-955e7bc2f513"
        controller.cars[0].player_id = "player1"
        
        # Simulate track data with car crossing finish line
        track_data = [1, 0, 0, 0, 0, 0, 0, 50, 1, 0, 25, 0, 0, 0, 0]
        
        await controller.handle_track_data(track_data)
        
        assert controller.track_power_status is True
        assert controller.port_current == 50
    
    @pytest.mark.asyncio
    async def test_handle_track_data_invalid_format(self, controller):
        """Test handling invalid track data format."""
        controller.current_race_state = config.RACE_STATE_GREEN_FLAG
        
        # Too short array
        await controller.handle_track_data([1, 2, 3])
        
        # Invalid values
        await controller.handle_track_data([256] * 15)
        
        # Should not crash
        assert True
    
    @pytest.mark.asyncio
    async def test_lap_time_processing(self, controller):
        """Test lap time processing."""
        controller.current_race_state = config.RACE_STATE_GREEN_FLAG
        controller.current_race_id = "5bb42be6-24cb-41ac-b1d8-955e7bc2f514"
        controller.cars[0].player_id = "player1"
        controller.cars[0].latest_finish_time = 0
        
        # Simulate car crossing finish line
        await controller._handle_car_lap(1, 50000)  # 50 second lap
        
        # Check if lap time was recorded
        lap_time = await controller.get_lap_time()
        
        assert lap_time is not None
        assert lap_time.race_id == "5bb42be6-24cb-41ac-b1d8-955e7bc2f514"
        assert lap_time.player_id == "player1"
        assert lap_time.time_ms == 50000
    
    def test_get_final_car_speed(self, controller):
        """Test final car speed calculation."""
        controller.current_race_state = config.RACE_STATE_GREEN_FLAG
        speed = controller._get_final_car_speed(50)
        assert speed == config.THROTTLE_SETTINGS[50]
        
        controller.current_race_state = config.RACE_STATE_YELLOW_FLAG
        speed = controller._get_final_car_speed(50)
        assert speed == config.THROTTLE_SETTINGS[config.YELLOW_FLAG_MAX_SPEED]
    
    def test_get_max_track_speed(self, controller):
        """Test maximum track speed calculation."""
        controller.current_race_state = config.RACE_STATE_GREEN_FLAG
        assert controller._get_max_track_speed() == 100
        
        controller.current_race_state = config.RACE_STATE_YELLOW_FLAG
        assert controller._get_max_track_speed() == config.YELLOW_FLAG_MAX_SPEED
        
        controller.current_race_state = config.RACE_STATE_RED_FLAG
        assert controller._get_max_track_speed() == 0
    
    @pytest.mark.asyncio
    async def test_generate_int_array(self, controller):
        """Test int array generation."""
        controller.cars[0].player_id = "player1"
        controller.cars[0].throttle = 50
        controller.cars[0].brakes_on_req = True
        
        await controller._generate_int_array()
        
        array = controller.get_current_int_array()
        assert len(array) == 9  # Expected array length
        assert array[0] == 255  # Operation mode
    
    def test_has_array_changed(self, controller):
        """Test array change detection."""
        # Initially should be changed
        assert controller.has_array_changed()
        
        # Second call should not be changed
        assert not controller.has_array_changed()
        
        # Modify array
        controller.current_int_array[0] = 100
        assert controller.has_array_changed()
    
    @pytest.mark.asyncio
    async def test_analytics_generation(self, controller):
        """Test analytics data generation."""
        controller.current_race_id = "test-race"
        controller.track_power_status = True
        controller.port_current = 75
        controller.cars[0].player_id = "player1"
        controller.cars[1].player_id = "player2"
        
        await controller._generate_analytics()
        
        analytics = await controller.get_analytics()
        assert analytics is not None
        assert analytics.race_id == "test-race"
        assert analytics.track_power_status is True
        assert analytics.port_current == 75
        assert analytics.active_cars == 2