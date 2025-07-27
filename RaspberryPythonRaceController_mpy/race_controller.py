"""
Main race controller logic
"""
import asyncio
import json
import config
from compat import ticks_ms, ticks_diff
from logger import log
from models import Car, LapTime, RaceAnalytics
from byte_helper import ByteHelper

class RaceController:
    """Main race controller managing cars and race state"""
    
    def __init__(self):
        """Initialize race controller"""
        self.current_race_id = config.INITIAL_RACE_ID
        self.current_int_array = config.INITIAL_INT_ARRAY.copy()
        self.previous_int_array = []
        self.current_race_state = None
        
        # Initialize cars
        self.cars = [Car(number=i+1) for i in range(config.TOTAL_NUMBER_OF_CARS)]
        
        # Queues for data processing
        self.lap_times_queue = asyncio.Queue(maxsize=100)
        self.analytics_queue = asyncio.Queue(maxsize=100)
        
        # Track status
        self.track_power_status = False
        self.port_current = 0
        self.previous_lap_time = None
        
        log.info("Race controller initialized")
    
    async def handle_race_update(self, json_string):
        """Process race state updates from MQTT"""
        try:
            data = json.loads(json_string)
            race_state = data.get("gameState")
            
            if race_state not in config.RACE_STATES:
                log.warning(f"Invalid race state: {race_state}")
                return
            
            log.info(f"Race state update: {race_state}")
            
            if race_state == config.RACE_STATE_LOBBY:
                await self._initialize_race(data)
            elif race_state == config.RACE_STATE_FORMATION_LAPS:
                await self._handle_formation_laps(data)
            
            # Reset finish times when leaving driving states
            if (self.current_race_state in config.RACE_DRIVING_STATES and 
                race_state not in config.RACE_DRIVING_STATES):
                self._reset_car_finish_times()
            
            self.current_race_state = race_state
            
            # Update car players for non-driving states
            if (race_state not in config.RACE_DRIVING_STATES and 
                race_state != config.RACE_STATE_FORMATION_LAPS):
                self._update_car_players(data)
            
            await self._generate_int_array()
            
        except Exception as e:
            log.error(f"Race update error: {e}")
    
    async def handle_car_update(self, json_string):
        """Process car control updates from MQTT"""
        try:
            data = json.loads(json_string)
            race_id = data.get("raceId")
            
            if race_id != self.current_race_id:
                log.warning(f"Race ID mismatch: {race_id} != {self.current_race_id}")
                return
            
            car_id = int(data.get("carId", 0)) - 1
            if 0 <= car_id < len(self.cars):
                # Update car attributes
                for key, value in data.items():
                    if hasattr(self.cars[car_id], key):
                        setattr(self.cars[car_id], key, value)
                
                log.debug(f"Updated car {car_id + 1}")
                await self._generate_int_array()
            
        except Exception as e:
            log.error(f"Car update error: {e}")
    
    async def handle_track_data(self, int_array):
        """Process data received from race track"""
        try:
            if self.current_race_state not in config.RACE_DRIVING_STATES:
                return
            
            # Extract track power status
            self.track_power_status = (int_array[0] & 1) != 0
            self.port_current = int_array[7]
            
            # Check for car crossing finish line
            car_id_crossed = int_array[8] & 7
            
            if 0 < car_id_crossed < 7:
                # Calculate game time from ticks
                game_ticks = 0
                for i in range(4):
                    game_ticks += int_array[9 + i] << (8 * i)
                
                game_time_ms = round(config.GAMETICK_IN_MILLISECOND * game_ticks)
                log.info(f"Car {car_id_crossed} crossed finish line at {game_time_ms}ms")
                
                await self._handle_car_lap(car_id_crossed, game_time_ms)
            
        except Exception as e:
            log.error(f"Track data error: {e}")
    
    async def _handle_car_lap(self, car_id, game_time_ms):
        """Process car lap completion"""
        car = self.cars[car_id - 1]
        last_time = car.latest_finish_time
        lap_time = game_time_ms - last_time
        
        if lap_time > config.MINIMUM_LAP_TIME_MS:
            lap_record = LapTime(self.current_race_id, car.player_id, lap_time)
            
            # Avoid duplicate lap times
            if self.previous_lap_time is None or self.previous_lap_time != lap_record:
                await self.lap_times_queue.put(lap_record)
                self.previous_lap_time = lap_record
                log.info(f"Lap time recorded: {lap_record}")
        
        car.latest_finish_time = game_time_ms
    
    async def _initialize_race(self, data):
        """Initialize new race"""
        race_id = data.get("raceId")
        self.current_race_id = race_id
        self.cars = [Car(number=i+1) for i in range(config.TOTAL_NUMBER_OF_CARS)]
        self.current_int_array = config.INITIAL_INT_ARRAY.copy()
        self.current_race_state = config.RACE_STATE_LOBBY
        log.info(f"Race initialized: {race_id}")
    
    async def _handle_formation_laps(self, data):
        """Handle formation lap configuration"""
        car_claims = data.get("carClaims", [])
        for claim in car_claims:
            car_id = claim.get("carId")
            if 1 <= car_id <= len(self.cars):
                car = self.cars[car_id - 1]
                formation_config = config.FORMATION_LAPS_CARS.get(car_id, {})
                
                if formation_config.get("enabled", False):
                    car.player_id = claim.get("playerId", "")
                    car.throttle = formation_config.get("throttle", 0)
                else:
                    car.player_id = ""
    
    def _update_car_players(self, data):
        """Update car player assignments"""
        car_claims = data.get("carClaims", [])
        for claim in car_claims:
            car_id = claim.get("carId")
            if 1 <= car_id <= len(self.cars):
                self.cars[car_id - 1].player_id = claim.get("playerId", "")
    
    def _reset_car_finish_times(self):
        """Reset all car finish times"""
        for car in self.cars:
            car.latest_finish_time = 0
    
    async def _generate_int_array(self):
        """Generate control array for race track"""
        array = [255]  # Operation mode
        
        led_helper = ByteHelper()
        
        # Process each car
        for i, car in enumerate(self.cars):
            if not car.player_id:
                array.append(255)  # Unclaimed car
                continue
            
            byte_helper = ByteHelper()
            led_helper.set_bit(i, 1)  # Car LED on
            
            if car.brakes_on_req:
                byte_helper.set_bit(7, 1)
            if car.lane_change_req:
                byte_helper.set_bit(6, 1)
            
            # Set car speed
            final_speed = self._get_final_car_speed(car.throttle)
            byte_helper.set_car_speed(final_speed)
            
            array.append(byte_helper.get_int_ones_complement())
        
        # Add game timer LED status
        timer_leds = self._get_timer_status_led()
        led_helper.set_bit(6, timer_leds[1])
        led_helper.set_bit(7, timer_leds[0])
        array.append(led_helper.number)
        
        # Add checksum
        array.append(ByteHelper.crc8(array))
        
        self.current_int_array = array
        log.debug(f"Generated int array: {array}")
    
    def _get_final_car_speed(self, throttle):
        """Calculate final car speed based on race state and throttle"""
        max_speed = self._get_max_track_speed()
        limited_throttle = min(throttle, max_speed)
        return config.THROTTLE_SETTINGS.get(limited_throttle, 0)
    
    def _get_max_track_speed(self):
        """Get maximum allowed speed based on race state"""
        if self.current_race_state in [config.RACE_STATE_GREEN_FLAG, config.RACE_STATE_PRACTICE]:
            return 100
        elif self.current_race_state == config.RACE_STATE_YELLOW_FLAG:
            return config.YELLOW_FLAG_MAX_SPEED
        return 0
    
    def _get_timer_status_led(self):
        """Get game timer LED status"""
        if self.current_race_state in config.RACE_DRIVING_STATES:
            return [1, 0]
        return [1, 1]
    
    async def get_lap_time(self):
        """Get next lap time from queue"""
        try:
            return await asyncio.wait_for(self.lap_times_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    async def get_analytics(self):
        """Get next analytics data from queue"""
        try:
            return await asyncio.wait_for(self.analytics_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    def get_current_int_array(self):
        """Get current control array for track"""
        return self.current_int_array
    
    def has_array_changed(self):
        """Check if control array has changed"""
        changed = self.current_int_array != self.previous_int_array
        if changed:
            self.previous_int_array = self.current_int_array.copy()
        return changed