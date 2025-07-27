"""
Data models for race controller
"""
import json
import config
from compat import ticks_ms

class Car:
    """Represents a slot car in the race"""
    
    def __init__(self, number, player_id="", throttle=0, lane_change_req=False, 
                 brakes_on_req=False, latest_finish_time=0):
        """Initialize car with default values"""
        self.number = number
        self.player_id = player_id
        self.throttle = throttle
        self.lane_change_req = lane_change_req
        self.brakes_on_req = brakes_on_req
        self.latest_finish_time = latest_finish_time
    
    def __eq__(self, other):
        """Check equality with another car"""
        return (self.number == other.number and 
                self.player_id == other.player_id and
                self.throttle == other.throttle and
                self.lane_change_req == other.lane_change_req and
                self.brakes_on_req == other.brakes_on_req and
                self.latest_finish_time == other.latest_finish_time)

class LapTime:
    """Represents a lap time record"""
    
    def __init__(self, race_id, player_id, lap_time_ms):
        """Initialize lap time record"""
        self.race_id = race_id
        self.player_id = player_id
        self.lap_time_ms = lap_time_ms
        self.timestamp = ticks_ms()
    
    def to_json(self):
        """Convert to JSON string for MQTT transmission"""
        return json.dumps({
            "raceId": self.race_id,
            "playerId": self.player_id,
            "timeInMilliSec": self.lap_time_ms
        })
    
    def __eq__(self, other):
        """Check equality with another lap time"""
        return (self.race_id == other.race_id and
                self.player_id == other.player_id and
                self.lap_time_ms == other.lap_time_ms)
    
    def __repr__(self):
        """String representation"""
        return f"{self.race_id}:{self.player_id}:{self.lap_time_ms}"

class RaceAnalytics:
    """Represents race analytics data"""
    
    def __init__(self, race_id, drive_int_array, slotcar_int_array):
        """Initialize analytics record"""
        self.race_id = race_id
        self.drive_int_array = drive_int_array
        self.slotcar_int_array = slotcar_int_array
        self.timestamp = ticks_ms()
    
    def to_json(self):
        """Convert to JSON string for MQTT transmission"""
        return json.dumps({
            "raceId": self.race_id,
            "driveIntArray": str(self.drive_int_array),
            "slotcarIntArray": str(self.slotcar_int_array),
            "timestamp": self.timestamp
        })