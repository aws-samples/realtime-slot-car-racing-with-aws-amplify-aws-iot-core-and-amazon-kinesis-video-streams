"""Main race controller logic with improved architecture."""
import asyncio
import logging
import time
from typing import List, Optional

from . import config
from .models import Car, LapTime, RaceAnalytics
from .security import SecurityValidator

logger = logging.getLogger(__name__)


class ByteHelper:
    """Helper class for byte operations."""
    
    def __init__(self):
        """Initialize byte helper."""
        self.number = 0
    
    def set_bit(self, position: int, value: int):
        """Set bit at position to value."""
        if value:
            self.number |= (1 << position)
        else:
            self.number &= ~(1 << position)
    
    def set_car_speed(self, speed: int):
        """Set car speed in lower 5 bits."""
        self.number = (self.number & 0xE0) | (speed & 0x1F)
    
    def get_int_ones_complement(self) -> int:
        """Get one's complement of the number."""
        return (~self.number) & 0xFF
    
    @staticmethod
    def crc8(data: List[int]) -> int:
        """Calculate CRC8 checksum."""
        crc = 0
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ 0x07
                else:
                    crc <<= 1
                crc &= 0xFF
        return crc


class RaceController:
    """Main race controller managing cars and race state."""
    
    def __init__(self):
        """Initialize race controller."""
        self.current_race_id = config.INITIAL_RACE_ID
        self.current_int_array = config.INITIAL_INT_ARRAY.copy()
        self.previous_int_array = []
        self.current_race_state: Optional[str] = None
        
        # Initialize cars
        self.cars: List[Car] = [Car(number=i+1) for i in range(config.TOTAL_NUMBER_OF_CARS)]
        
        # Queues for data processing
        self.lap_times_queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        self.analytics_queue: asyncio.Queue = asyncio.Queue(maxsize=100)
        
        # Track status
        self.track_power_status = False
        self.port_current = 0
        self.previous_lap_time: Optional[LapTime] = None
        
        logger.info("Race controller initialized")
    
    async def handle_race_update(self, json_string: str):
        """
        Process race state updates from MQTT.
        
        Args:
            json_string: JSON string containing race update data
        """
        try:
            # Validate and parse JSON safely
            data = SecurityValidator.validate_json_input(json_string)
            race_state = data.get("gameState")
            
            if race_state not in config.RACE_STATES:
                logger.warning(f"Invalid race state: {race_state}")
                return
            
            logger.info(f"Race state update: {race_state}")
            
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
            logger.error(f"Race update error: {e}")
    
    async def handle_car_update(self, json_string: str):
        """
        Process car control updates from MQTT.
        
        Args:
            json_string: JSON string containing car update data
        """
        try:
            # Validate and parse JSON safely
            data = SecurityValidator.validate_json_input(json_string)
            race_id = data.get("raceId")
            
            # Validate race ID
            if not SecurityValidator.validate_race_id(race_id) or race_id != self.current_race_id:
                logger.warning(f"Invalid or mismatched race ID: {race_id}")
                return
            
            # Validate car ID
            if not SecurityValidator.validate_car_id(data.get("carId")):
                logger.warning(f"Invalid car ID: {data.get('carId')}")
                return
            
            car_id = int(data.get("carId")) - 1
            
            # Sanitize car update data
            sanitized_data = SecurityValidator.sanitize_car_update(data)
            
            # Apply sanitized updates
            for key, value in sanitized_data.items():
                setattr(self.cars[car_id], key, value)
            
            logger.debug(f"Updated car {car_id + 1}")
            await self._generate_int_array()
            
        except Exception as e:
            logger.error(f"Car update error: {e}")
    
    async def handle_track_data(self, int_array: List[int]):
        """
        Process data received from race track.
        
        Args:
            int_array: List of integers from track controller
        """
        try:
            if self.current_race_state not in config.RACE_DRIVING_STATES:
                return
            
            # Validate input array
            if not isinstance(int_array, list) or len(int_array) < 15:
                logger.warning("Invalid track data format")
                return
            
            # Validate array values are within byte range
            if not all(isinstance(x, int) and 0 <= x <= 255 for x in int_array):
                logger.warning("Invalid track data values")
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
                logger.info(f"Car {car_id_crossed} crossed finish line at {game_time_ms}ms")
                
                await self._handle_car_lap(car_id_crossed, game_time_ms)
            
            # Generate analytics data
            await self._generate_analytics()
            
        except Exception as e:
            logger.error(f"Track data error: {e}")
    
    async def _handle_car_lap(self, car_id: int, game_time_ms: int):
        """
        Process car lap completion.
        
        Args:
            car_id: ID of car that completed lap
            game_time_ms: Game time in milliseconds
        """
        car = self.cars[car_id - 1]
        last_time = car.latest_finish_time
        lap_time = game_time_ms - last_time
        
        if lap_time > config.MINIMUM_LAP_TIME_MS:
            lap_record = LapTime(self.current_race_id, car.player_id, lap_time)
            
            # Avoid duplicate lap times
            if self.previous_lap_time is None or self.previous_lap_time != lap_record:
                await self.lap_times_queue.put(lap_record)
                self.previous_lap_time = lap_record
                logger.info(f"Lap time recorded: {lap_record}")
        
        car.latest_finish_time = game_time_ms
    
    async def _initialize_race(self, data: dict):
        """
        Initialize new race.
        
        Args:
            data: Race initialization data
        """
        race_id = data.get("raceId")
        
        # Validate race ID
        if not SecurityValidator.validate_race_id(race_id):
            logger.warning(f"Invalid race ID format: {race_id}")
            return
        
        self.current_race_id = race_id
        self.cars = [Car(number=i+1) for i in range(config.TOTAL_NUMBER_OF_CARS)]
        self.current_int_array = config.INITIAL_INT_ARRAY.copy()
        self.current_race_state = config.RACE_STATE_LOBBY
        logger.info(f"Race initialized: {race_id}")
    
    async def _handle_formation_laps(self, data: dict):
        """
        Handle formation lap configuration.
        
        Args:
            data: Formation lap data
        """
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
    
    def _update_car_players(self, data: dict):
        """
        Update car player assignments.
        
        Args:
            data: Car player assignment data
        """
        car_claims = data.get("carClaims", [])
        for claim in car_claims:
            car_id = claim.get("carId")
            if 1 <= car_id <= len(self.cars):
                self.cars[car_id - 1].player_id = claim.get("playerId", "")
    
    def _reset_car_finish_times(self):
        """Reset all car finish times."""
        for car in self.cars:
            car.latest_finish_time = 0
    
    async def _generate_int_array(self):
        """Generate control array for race track."""
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
        logger.debug(f"Generated int array: {array}")
    
    async def _generate_analytics(self):
        """Generate race analytics data."""
        active_cars = sum(1 for car in self.cars if car.player_id)
        
        analytics = RaceAnalytics(
            race_id=self.current_race_id,
            track_power_status=self.track_power_status,
            port_current=self.port_current,
            active_cars=active_cars
        )
        
        try:
            await self.analytics_queue.put(analytics)
        except asyncio.QueueFull:
            logger.warning("Analytics queue full, dropping data")
    
    def _get_final_car_speed(self, throttle: int) -> int:
        """
        Calculate final car speed based on race state and throttle.
        
        Args:
            throttle: Requested throttle value
            
        Returns:
            Final speed value
        """
        max_speed = self._get_max_track_speed()
        limited_throttle = min(throttle, max_speed)
        return config.THROTTLE_SETTINGS.get(limited_throttle, 0)
    
    def _get_max_track_speed(self) -> int:
        """
        Get maximum allowed speed based on race state.
        
        Returns:
            Maximum speed value
        """
        if self.current_race_state in [config.RACE_STATE_GREEN_FLAG, config.RACE_STATE_PRACTICE]:
            return 100
        elif self.current_race_state == config.RACE_STATE_YELLOW_FLAG:
            return config.YELLOW_FLAG_MAX_SPEED
        return 0
    
    def _get_timer_status_led(self) -> List[int]:
        """
        Get game timer LED status.
        
        Returns:
            List of LED status values
        """
        if self.current_race_state in config.RACE_DRIVING_STATES:
            return [1, 0]
        return [1, 1]
    
    async def get_lap_time(self) -> Optional[LapTime]:
        """
        Get next lap time from queue.
        
        Returns:
            LapTime object or None if no data
        """
        try:
            return await asyncio.wait_for(self.lap_times_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    async def get_analytics(self) -> Optional[RaceAnalytics]:
        """
        Get next analytics data from queue.
        
        Returns:
            RaceAnalytics object or None if no data
        """
        try:
            return await asyncio.wait_for(self.analytics_queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            return None
    
    def get_current_int_array(self) -> List[int]:
        """
        Get current control array for track.
        
        Returns:
            Current control array
        """
        return self.current_int_array
    
    def has_array_changed(self) -> bool:
        """
        Check if control array has changed.
        
        Returns:
            True if array changed, False otherwise
        """
        changed = self.current_int_array != self.previous_int_array
        if changed:
            self.previous_int_array = self.current_int_array.copy()
        return changed