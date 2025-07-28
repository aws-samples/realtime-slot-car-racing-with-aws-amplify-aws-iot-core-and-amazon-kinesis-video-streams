"""
Test script for RaceController functionality
"""
import sys
sys.path.append('..')

import json
import asyncio
from race_controller import RaceController
import config

async def test_race_initialization():
    """Test race initialization"""
    print("Testing race initialization...")
    
    controller = RaceController()
    
    # Test initial state
    assert controller.current_race_id == config.INITIAL_RACE_ID, "Initial race ID should be set"
    assert len(controller.cars) == config.TOTAL_NUMBER_OF_CARS, "Should have correct number of cars"
    
    # Test race update
    race_data = {
        "gameState": "lobby",
        "raceId": "2bb42be6-24cb-41ac-b1d8-955e7bc2f511",
        "carClaims": []
    }
    
    await controller.handle_race_update(json.dumps(race_data))
    
    assert controller.current_race_id == "2bb42be6-24cb-41ac-b1d8-955e7bc2f511", "Race ID should be updated"
    assert controller.current_race_state == config.RACE_STATE_LOBBY, "Race state should be lobby"
    
    print("✓ Race initialization test passed")

async def test_car_updates():
    """Test car control updates"""
    print("Testing car updates...")
    
    controller = RaceController()
    
    # Set up race first
    race_data = {
        "gameState": "lobby",
        "raceId": "3bb42be6-24cb-41ac-b1d8-955e7bc2f512",
        "carClaims": []
    }
    await controller.handle_race_update(json.dumps(race_data))
    
    # Test car update
    car_data = {
        "raceId": "3bb42be6-24cb-41ac-b1d8-955e7bc2f512",
        "carId": "1",
        "player_id": "player123",
        "throttle": 75,
        "lane_change_req": True,
        "brakes_on_req": False
    }
    
    await controller.handle_car_update(json.dumps(car_data))
    
    car = controller.cars[0]  # Car 1 is index 0
    assert car.player_id == "player123", "Player ID should be updated"
    assert car.throttle == 75, "Throttle should be updated"
    assert car.lane_change_req == True, "Lane change should be updated"
    assert car.brakes_on_req == False, "Brakes should be updated"
    
    print("✓ Car updates test passed")

async def test_int_array_generation():
    """Test control array generation"""
    print("Testing int array generation...")
    
    controller = RaceController()
    controller.current_race_state = config.RACE_STATE_GREEN_FLAG
    
    # Set up a car
    controller.cars[0].player_id = "player1"
    controller.cars[0].throttle = 50
    controller.cars[0].lane_change_req = True
    
    await controller._generate_int_array()
    
    int_array = controller.get_current_int_array()
    
    assert len(int_array) == 9, "Array should have 9 elements"
    assert int_array[0] == 255, "First element should be operation mode"
    assert int_array[-1] != 0, "Last element should be checksum"
    
    print(f"✓ Int array generation test passed (array: {int_array})")

async def test_lap_time_processing():
    """Test lap time processing"""
    print("Testing lap time processing...")
    
    controller = RaceController()
    controller.current_race_state = config.RACE_STATE_GREEN_FLAG
    controller.current_race_id = "4bb42be6-24cb-41ac-b1d8-955e7bc2f513"
    
    # Set up car with player
    controller.cars[0].player_id = "player1"
    controller.cars[0].latest_finish_time = 0
    
    # Simulate car crossing finish line
    await controller._handle_car_lap(1, 50000)  # 50 second lap
    
    # Check if lap time was recorded
    lap_time = await controller.get_lap_time()
    
    assert lap_time is not None, "Lap time should be recorded"
    assert lap_time.race_id == "4bb42be6-24cb-41ac-b1d8-955e7bc2f513", "Race ID should match"
    assert lap_time.player_id == "player1", "Player ID should match"
    assert lap_time.lap_time_ms == 50000, "Lap time should be correct"
    
    print("✓ Lap time processing test passed")

async def test_track_data_processing():
    """Test track data processing"""
    print("Testing track data processing...")
    
    controller = RaceController()
    controller.current_race_state = config.RACE_STATE_GREEN_FLAG
    controller.current_race_id = "5bb42be6-24cb-41ac-b1d8-955e7bc2f514"
    
    # Set up car
    controller.cars[0].player_id = "player1"
    
    # Simulate track data with car 1 crossing finish line
    track_data = [
        255,  # Track status
        255, 255, 255, 255, 255, 255,  # Car data
        24,   # Port current
        249,  # Car ID (248 ^ 1 = 249 for car 1)
        0x40, 0x42, 0x0F, 0x00,  # Game ticks (1000000 ticks)
        0,    # Buttons
        0     # Checksum (will be ignored in test)
    ]
    
    await controller.handle_track_data(track_data)
    
    # Check if track status was updated
    assert controller.track_power_status == True, "Track power should be on"
    assert controller.port_current == 24, "Port current should be updated"
    
    print("✓ Track data processing test passed")

async def run_all_tests():
    """Run all RaceController tests"""
    print("=== RaceController Tests ===")
    
    try:
        await test_race_initialization()
        await test_car_updates()
        await test_int_array_generation()
        await test_lap_time_processing()
        await test_track_data_processing()
        
        print("\n✅ All RaceController tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(run_all_tests())